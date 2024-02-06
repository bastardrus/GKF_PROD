import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

def replace_variables(command, serial_number, cell_name):
    replaced_command = command.replace("{serial_number}", f"{{{serial_number}}}").replace("{cell_name}", f"{{{cell_name}}}")
    return replaced_command

def process_commands(input_file_path, output_file_path, serial_number, cell_name):
    with open(input_file_path, "r") as input_file:
        commands = input_file.readlines()

    replaced_commands = []
    for command in commands:
        replaced_command = replace_variables(command, serial_number, cell_name)
        replaced_commands.append(replaced_command)

    with open(output_file_path, "w") as output_file:
        for replaced_command in replaced_commands:
            output_file.write(replaced_command)

def home(request):
    if request.method == 'POST':
        spisok_file = request.FILES['spisok_file']
        serial_number = request.POST['serial_number']
        cell_name = request.POST['cell_name']

        upload_dir = os.path.join(settings.BASE_DIR, 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        spisok_file_path = os.path.join(upload_dir, spisok_file.name)
        with open(spisok_file_path, 'wb+') as destination:
            for chunk in spisok_file.chunks():
                destination.write(chunk)

        output_file_name = f"{cell_name}_MML.txt"
        output_file_path = os.path.join(upload_dir, output_file_name)

        process_commands(spisok_file_path, output_file_path, serial_number, cell_name)

        with open(output_file_path, 'rb') as output_file:
            response = HttpResponse(output_file, content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename={output_file_name}'
            return response

    return render(request, 'gkf_app/home.html')
