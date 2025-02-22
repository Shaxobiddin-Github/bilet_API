import sys

if sys.platform == "win32":
    import pythoncom  # Faqat Windows uchun

from django.shortcuts import render
from django.http import JsonResponse


import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from docx import Document
from docx2pdf import convert
from PyPDF2 import PdfMerger
import pythoncom  # COM uchun kerakli modul
import random
from .models import File
from django.conf import settings
from rest_framework.parsers import MultiPartParser
from openpyxl import load_workbook
from django.test import Client  # Test clientdan foydalanamiz
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated







class UploadQuestions(APIView):
    parser_classes = [MultiPartParser]

    permission_classes = [IsAuthenticated]
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "Fayl topilmadi!"}, status=400)

        # Faylni saqlash
        file_path = os.path.join(settings.MEDIA_ROOT, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Foydalanuvchidan ustun indekslarini olish (1=B, 2=C, va hokazo)
        try:
            column_easy = int(request.data.get('column_easy', 2)) - 1  # B ustuni standart (2)
            column_medium = int(request.data.get('column_medium', 3)) - 1  # C ustuni standart (3)
            column_murakkab1 = int(request.data.get('column_murakkab1', 4)) - 1  # D ustuni standart (4)
            column_murakkab2 = int(request.data.get('column_murakkab2', 5)) - 1  # E ustuni standart (5)
            column_hard = int(request.data.get('column_hard', 6)) - 1  # F ustuni standart (6)
        except (ValueError, TypeError):
            return Response({"error": "Ustun indekslari to'g'ri son bo'lishi kerak!"}, status=400)

        # Excel faylni o‘qish
        try:
            workbook = load_workbook(file_path)
            sheet = workbook.active

            # Savollarni darajalar bo‘yicha ajratish
            questions_easy = []
            questions_medium = []
            questions_murakkab1 = []
            questions_murakkab2 = []
            questions_hard = []

            # 1-qator va A ustunini tashlab ketish uchun min_row=2 dan boshlaymiz
            for row in sheet.iter_rows(min_row=2, min_col=2, values_only=True):
                if len(row) > max(column_easy, column_medium, column_murakkab1, column_murakkab2, column_hard):
                    if column_easy >= 0 and row[column_easy] is not None:
                        questions_easy.append(row[column_easy])
                    if column_medium >= 0 and row[column_medium] is not None:
                        questions_medium.append(row[column_medium])
                    if column_murakkab1 >= 0 and row[column_murakkab1] is not None:
                        questions_murakkab1.append(row[column_murakkab1])
                    if column_murakkab2 >= 0 and row[column_murakkab2] is not None:
                        questions_murakkab2.append(row[column_murakkab2])
                    if column_hard >= 0 and row[column_hard] is not None:
                        questions_hard.append(row[column_hard])

            # JSON fayllarga saqlash
            json_files = {
                "easy": questions_easy,
                "medium": questions_medium,
                "murakkab1": questions_murakkab1,
                "murakkab2": questions_murakkab2,
                "hard": questions_hard,
            }

            for difficulty, questions in json_files.items():
                output_path = os.path.join(settings.MEDIA_ROOT, f"{difficulty}_questions.json")
                with open(output_path, "w", encoding="utf-8") as json_file:
                    json.dump(questions, json_file, ensure_ascii=False, indent=4)

        except Exception as e:
            return Response({"error": f"Faylni o'qishda xatolik: {str(e)}"}, status=500)

        # Biletlar va savollar sonini default holatda belgilash
        try:
            num_tickets = int(request.data.get('num_tickets', 1))  # Default 5 ta bilet
        except (ValueError, TypeError):
            return Response({"error": "Biletlar soni to'g'ri son bo'lishi kerak!"}, status=400)

        if num_tickets < 1:
            return Response({"error": "Biletlar soni kamida 1 ta bo'lishi kerak!"}, status=400)
        num_easy = 1     # Default Easy’dan 1 ta
        num_medium = 1   # Default Medium’dan 1 ta
        num_murakkab1 = 1  # Default Murakkab1’dan 1 ta
        num_murakkab2 = 1  # Default Murakkab2’dan 1 ta
        num_hard = 1     # Default Hard’dan 1 ta

        # Avtomatik ravishda biletlarni yaratish
        client = Client()
        generate_url = reverse('generate_tickets')
        client.post(generate_url, data={
            "num_tickets": num_tickets,
            "num_easy": num_easy,
            "num_medium": num_medium,
            "num_murakkab1": num_murakkab1,
            "num_murakkab2": num_murakkab2,
            "num_hard": num_hard
        }, content_type="application/json")

        # Eksport qilish
        export_url = reverse('export_tickets')
        client.get(export_url)

        return Response({
            "message": f"Savollar yuklandi, {num_tickets} ta biletlar yaratildi va PDFga eksport qilindi!",
            "files": [
                f"{settings.MEDIA_URL}easy_questions.json",
                f"{settings.MEDIA_URL}medium_questions.json",
                f"{settings.MEDIA_URL}murakkab1_questions.json",
                f"{settings.MEDIA_URL}murakkab2_questions.json",
                f"{settings.MEDIA_URL}hard_questions.json",
            ]
        })






    
class GenerateTickets(APIView):
    def post(self, request):
        # Foydalanuvchidan kelgan ma'lumotlardan nechtadan bilet yaratish kerakligini olish
        num_tickets = request.data.get('num_tickets', 1)  # Nechta bilet yaratish, standart 1 ta

        # Har bir darajadan nechtadan savol olish kerakligini olish
        num_easy = request.data.get('num_easy', 1)
        num_medium = request.data.get('num_medium', 1)
        num_murakkab1 = request.data.get('num_murakkab1', 1)
        num_murakkab2 = request.data.get('num_murakkab2', 1)
        num_hard = request.data.get('num_hard', 1)

        # Jami savollar sonini hisoblash
        total_requested = num_easy + num_medium + num_murakkab1 + num_murakkab2 + num_hard

        if total_requested != 5:
            return Response({"error": "Har bir bilet uchun jami savollar soni 5 ta bo'lishi kerak!"}, status=400)

        # Agar num_tickets noto'g'ri bo'lsa (masalan, manfiy yoki 0)
        if num_tickets < 1:
            return Response({"error": "Biletlar soni kamida 1 ta bo'lishi kerak!"}, status=400)

        # JSON fayllaridan savollarni o'qish
        try:
            question_files = {
                "easy": os.path.join(settings.MEDIA_ROOT, "easy_questions.json"),
                "medium": os.path.join(settings.MEDIA_ROOT, "medium_questions.json"),
                "murakkab1": os.path.join(settings.MEDIA_ROOT, "murakkab1_questions.json"),
                "murakkab2": os.path.join(settings.MEDIA_ROOT, "murakkab2_questions.json"),
                "hard": os.path.join(settings.MEDIA_ROOT, "hard_questions.json"),
            }

            questions = {}
            for level, path in question_files.items():
                with open(path, "r", encoding="utf-8") as f:
                    questions[level] = json.load(f)

            # Har bir darajada kamida bitta savol borligini tekshiramiz
            if any(not q for q in questions.values()):
                return Response({"error": "Tanlash uchun yetarli savollar mavjud emas!"}, status=400)

        except FileNotFoundError:
            return Response({"error": "JSON fayllari topilmadi! Avval savollarni yuklang."}, status=400)

        # Biletlarni yaratish
        tickets = []
        try:
            for _ in range(num_tickets):
                ticket = {"easy": [], "medium": [], "murakkab1": [], "murakkab2": [], "hard": []}
                all_levels = ["easy", "medium", "murakkab1", "murakkab2", "hard"]
                num_per_level = [num_easy, num_medium, num_murakkab1, num_murakkab2, num_hard]

                # Har bir darajadan faqat 1 ta savolni o'z joyiga qo'yamiz
                for level, num in zip(all_levels, num_per_level):
                    if questions[level]:  # Agar savollar mavjud bo'lsa
                        ticket[level].append(random.choice(questions[level]))  # Faqat 1 ta tasodifiy savol

                # Qolgan 4 ta joyni tasodifiy boshqa darajalardan to'ldiramiz
                remaining_slots = 4  # Jami 5 ta, 1 tasi allaqachon har bir darajaga qo'yilgan
                all_questions = [q for level in questions.values() for q in level if q not in [item for sublist in ticket.values() for item in sublist]]

                available_levels = [l for l in all_levels if l not in [k for k, v in ticket.items() if v]]  # Bo'sh darajalar

                while remaining_slots > 0 and all_questions and available_levels:
                    level = random.choice(available_levels)
                    if all_questions:
                        ticket[level].append(all_questions.pop(0))
                        if ticket[level]:  # Agar bu daraja endi bo'sh emas bo'lsa
                            available_levels.remove(level)
                        remaining_slots -= 1

                # Har bir darajada kamida 1 ta savol bo'lishini ta'minlash
                for level in all_levels:
                    if not ticket[level] and all_questions:
                        ticket[level].append(all_questions.pop(0))

                # Agar hali ham 5 taga yetmagan bo'lsa, xato qaytarish
                if sum(len(v) for v in ticket.values()) != 5:
                    return Response({"error": "Tanlash uchun yetarli savollar mavjud emas!"}, status=400)

                tickets.append(ticket)

        except (IndexError, ValueError):
            return Response({"error": "Tanlash uchun yetarli savollar mavjud emas!"}, status=400)

        # Natijani JSON fayliga saqlash
        tickets_output_path = os.path.join(settings.MEDIA_ROOT, "tickets_output.json")
        with open(tickets_output_path, "w", encoding="utf-8") as f:
            json.dump({"tickets": tickets}, f, ensure_ascii=False, indent=4)

        return Response({
            "message": f"{num_tickets} ta biletlar yaratildi!",
            "files": [
                f"{settings.MEDIA_URL}tickets_output.json"
            ],
            "tickets": tickets
        })






class ExportTickets(APIView):
    def get(self, request):
        # COM ob'ektini boshlash
        pythoncom.CoInitialize()

        tickets_output_path = os.path.join(settings.MEDIA_ROOT, "tickets_output.json")

        try:
            # JSON faylni o'qish
            with open(tickets_output_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return Response({"error": "output.json fayli topilmadi!"}, status=404)

        tickets = data.get("tickets", [])
        if not tickets:
            return Response({"error": "Biletlar topilmadi!"}, status=400)

        # Static papkadagi Word shablon fayli yo'li
        template_path = os.path.join(os.path.dirname(__file__), '../static/bilet_savollar.docx')

        # Fayl mavjudligini tekshirish
        if not os.path.exists(template_path):
            return Response({"error": f"Word shablon fayli topilmadi! Yo'l: {template_path}"}, status=404)

        # Fayllarni saqlash uchun katalog
        output_dir = r"D:\Snayder\bilet_API\media"
        os.makedirs(output_dir, exist_ok=True)  # Agar katalog mavjud bo'lmasa, uni yaratamiz

        word_files = []

        # Har bir biletni qayta ishlash
        for ticket_num, ticket in enumerate(tickets, start=1):
            # Word faylni yaratish
            doc = Document(template_path)

            # Jadvalni tekshirish
            if not doc.tables:
                return Response({"error": "Word shablonida jadval mavjud emas!"}, status=500)

            table = doc.tables[0]  # Birinchi jadvalni tanlash

            # Savollarni jadvalga yozish
            questions = list(ticket.values())  # Biletdagi savollarni ro'yxatga aylantirish
            for i, question in enumerate(questions):
                if i < len(table.rows):  # Jadvalning mos qatori mavjudligini tekshirish
                    table.rows[i].cells[1].text = question  # Jadvalning 2-ustuniga savolni yozish

            # Fayl nomini dinamik ravishda yaratish
            output_file = os.path.join(output_dir, f"bilet_{ticket_num}.docx")
            doc.save(output_file)
            word_files.append(output_file)

        # Word fayllarni PDFga aylantirish
        pdf_files = []
        for word_file in word_files:
            pdf_file = word_file.replace(".docx", ".pdf")
            convert(word_file)  # Word -> PDF konvertatsiyasi
            pdf_files.append(pdf_file)

        # PDF fayllarni birlashtirish
        merged_pdf = os.path.join(output_dir, "merged_tickets.pdf")
        merger = PdfMerger()
        for pdf in pdf_files:
            merger.append(pdf)
        merger.write(merged_pdf)
        merger.close()


        samdu_instance = File.objects.create(file=f"pdf_files/merged_tickets.pdf")
    
        # COM ob'ektini tozalash
        pythoncom.CoUninitialize()

        return Response({
            "message": "Biletlar PDFga aylantirildi!",
            "merged_pdf": f"{merged_pdf}"
        })