web=0
data=0
cyber=0
cloud=0
print("Please choose the answer that best reflects your preferences.")

print("======================================")
print("1. I enjoy creating visually appealing and interactive experiences.")
print("2. I am curious about uncovering hidden patterns and insights from data.")
print("3. I am fascinated by the challenge of protecting systems and information from threats.")
print("4. I am interested in designing and managing scalable and reliable IT infrastructure.")
print("5. I find working with code and building software applications stimulating.")
print("6. I am analytical and enjoy solving complex problems using logic and reasoning.")
print("7. I am detail-oriented and enjoy troubleshooting technical issues.")
print("8. I am comfortable working with cutting-edge technologies and cloud platforms.")
print("======================================")
no1=int(input("enter your number: "))
if no1 == 1 or no1 == 5 or no1 == 7:
    web+=2
if no1 == 2 or no1 == 5 or no1 == 6:
    data+=2
if no1 == 3 or no1 == 6 or no1 == 7 or no1==8:
    cyber+=2
if no1 == 4 or no1 == 8:
    cloud+=2


print("==================================")
print("Strength analysis:")
print("1. I am highly creative and possess a strong sense of design aesthetics.")
print("2. I am comfortable with mathematics, statistics, and problem-solving techniques.")
print("3. I am logical and have a keen eye for detail. ")
print("4. I am a quick learner and can adapt to new technologies quickly.")
print("5. I am a strong communicator and enjoy working collaboratively.")
print("==================================")

no2=int(input("enter your first number: "))
if no2 == 1 or no2 == 4 or no2 == 5:
    web+=3
if no2 == 2 or no2 == 4 or no2 == 5:
    data+=3
if no2 == 3 or no2 == 4 or no2 == 5:
    cyber+=3
if no2 == 3 or no2 == 4 or no2 == 5:
    cloud+=3

print("==================================")
print("Weakness Analysis")
print("1. I find repetitive tasks tedious.")
print("2. I am not comfortable with complex mathematical concepts.")
print("3. I dislike working with tight deadlines and pressure.")
print("4. I am not comfortable with public speaking or presentations.")

no3=int(input("enter your first number: "))
if no3 == 1 or no3 == 2:
    web+=1
if no3 == 1 or no3 == 4:
    data+=1
if no3 == 3:
    cyber+=1
if no3 == 4:
    cloud+=1



w = input("Do you enjoy working on creative projects with a visual component (e.g., designing websites, user interfaces)? :")
if w =="y":
    web+=2
else:
    web-=1
d = input("Can you explain a complex concept in a clear and concise way to someone with no technical background?: ")
if d =="y":
    data+=2
else:
    data-=1
cs = input("Are you comfortable working independently and taking initiative to solve problems?: ")
if cs =="y":
    cyber+=2
else:
    cyber-=1
ce = input("Do you enjoy staying up-to-date with the latest advancements in cloud technologies?: ")
if cs =="y":
    cloud+=2
else:
    cloud-=1



print([data,web,cyber,cloud])



