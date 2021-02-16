import csv


with open('users.csv', 'w', newline='') as f:
  writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  writer.writerow(['first_name', 'last_name', 'email', 'password',])

  for i in range(1, 9, 1):
    first_name = f'F{str(i).zfill(3)}'
    last_name = f'L{str(i).zfill(3)}'
    email = f'daichi.yoshikawa+{str(i).zfill(3)}@gmail.com'
    password = 'testtest'
    writer.writerow([first_name, last_name, email, password,])
