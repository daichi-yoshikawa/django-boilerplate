import csv


with open('tenant_users.csv', 'w', newline='') as f:
  writer = csv.writer(f, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  writer.writerow(['tenant_id', 'user_id'])

  writer.writerow([1, 1])
  writer.writerow([2, 2])
  writer.writerow([3, 3])
  writer.writerow([1, 4])
  writer.writerow([2, 4])
  writer.writerow([1, 5])
  writer.writerow([3, 5])
  writer.writerow([2, 6])
  writer.writerow([3, 6])
  writer.writerow([1, 7])
  writer.writerow([2, 7])
  writer.writerow([3, 7])
