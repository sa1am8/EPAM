from math import sqrt

#sides
side_a = 4.5
side_b = 5.9
side_c = 9

#for Heron's formula - S = sqrt(p(p-a)(p-b)(p-c)), p = (a+b+c)/2
def Heron(a,b,c):
    p = (a+b+c)/2
    return round(sqrt(p*(p-a)*(p-b)*(p-c)),2)

if __name__ == '__main__':
    print(Heron(side_a,side_b,side_c))