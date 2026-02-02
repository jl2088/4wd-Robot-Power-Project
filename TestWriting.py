arr = [0]*10

for i in range(10):
    arr[i] = 3 * i

with open('./log.txt', 'w') as file:
    for j in range(10):
        file.write(f"The number is: {arr[j]}\n")
    file.write("Hello, World!\n")
    file.write("--Pico.")