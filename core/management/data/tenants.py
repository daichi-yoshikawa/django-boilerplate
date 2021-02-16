import csv


with open('tenants.csv', 'w', newline='') as f:
  writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  writer.writerow(['name',])

  for i in range(1, 4, 1):
    name = f'Tenant{str(i).zfill(3)}'
    writer.writerow([name,])

