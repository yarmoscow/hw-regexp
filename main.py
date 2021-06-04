from pprint import pprint
import re
import csv

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


# Разбираем файл

first_line = True
contacts_list_temp_dict = dict()
for contact in contacts_list:
    if first_line:
        first_line = False
        continue

    first_name = ''
    middle_name = ''

    # разбираем поле lastname
    last_name_match = re.match("([-A-ЯЁа-яё]+)\s{0,1}([-A-ЯЁа-яё]*)\s{0,1}([-A-ЯЁа-яё]*)", contact[0])
    last_name = last_name_match.group(1)
    first_name = last_name_match.group(2) if last_name_match.group(2) else ''
    middle_name = last_name_match.group(3) if last_name_match.group(3) else ''

    first_name_match = re.match("([-A-ЯЁа-яё]+)\s{0,1}([-A-ЯЁа-яё]*)", contact[1])
    if first_name_match:
        first_name = first_name_match.group(1) if not first_name and first_name_match.group(1) else first_name
        middle_name = first_name_match.group(2) if not middle_name and first_name_match.group(2) else middle_name

    middle_name = contact[2] if not middle_name else middle_name
    organization = contact[3]
    position = contact[4]
    phone = contact[5]
    
    if phone:
        phone = re.sub("^8", "+7", contact[5])
        phone = re.sub("\s|-|\(|\)", "", phone)
        phone_match = re.match("\+7(\d{3})(\d{3})(\d{2})(\d{2})(доб.)?(\d{4})?", phone)
        phone = "+7 (" + phone_match.group(1) + ") " + phone_match.group(2) + "-" + phone_match.group(3) + "-" + phone_match.group(4)
        if phone_match.group(6):
            phone += " доб." + phone_match.group(6)

    email = contact[6]
    contacts_list_temp_dict_key = last_name + " " +first_name

    # Если уже есть запись с такими фамилией и именем, то приоритетно используем новые значения.
    if contacts_list_temp_dict.get(contacts_list_temp_dict_key):
        middle_name = middle_name if middle_name else contacts_list_temp_dict[contacts_list_temp_dict_key][2]
        organization = organization if organization else contacts_list_temp_dict[contacts_list_temp_dict_key][3]
        position = position if position else contacts_list_temp_dict[contacts_list_temp_dict_key][4]
        phone = phone if phone else contacts_list_temp_dict[contacts_list_temp_dict_key][5]
        email = email if email else contacts_list_temp_dict[contacts_list_temp_dict_key][6]
    else:
        1

    contacts_list_temp_dict |= {contacts_list_temp_dict_key: [last_name, first_name, middle_name, organization, position, phone, email]}

# дебаг, посмотреть что получается.
# pprint(contacts_list_temp_dict)


# сохраняем получившиеся данные в другой файл
with open("phonebook.csv", "w", encoding='utf-8', newline='\n') as f:
    data_writer = csv.writer(f, delimiter=',')

    # в примере ошибка, surname - это фамилия, а отчество - middle name. Вывод будем делать правильно.
    data_writer.writerow(['lastname', 'firstname', 'middlename', 'organization', 'position', 'phone', 'email'])
    data_writer.writerows(contacts_list_temp_dict.values())

