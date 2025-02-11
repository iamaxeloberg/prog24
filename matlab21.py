import numpy as np
import matplotlib.pyplot as plt

def dydx(x, y):
    """Differentialekvationen y'(x)"""
    return -((1/6) + (np.pi * np.sin(np.pi*x))/(1.6 - np.cos(np.pi*x))) * y

def euler_method(h, x_end=4.0, y0=2.5):
    """
    Implementerar Eulers metod
    h: steglängd
    x_end: slutvärde för x
    y0: startvärde y(0)
    """
    x = np.arange(0, x_end + h, h)
    y = np.zeros(len(x))
    y[0] = y0
    
    for i in range(1, len(x)):
        y[i] = y[i-1] + h * dydx(x[i-1], y[i-1])
    
    return x, y

# a) Beräkna med olika steglängder och plotta
steglangder = [0.5, 0.25, 0.1, 0.05]
plt.figure(figsize=(12, 6))

for h in steglangder:
    x, y = euler_method(h)
    plt.plot(x, y, label=f'h = {h}')
    print(f'y(4) med h = {h}: {y[-1]:.6f}')

plt.grid(True)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Lösning med olika steglängder')
plt.legend()
plt.show()

# b) Beräkna konvergens och felgräns
def find_convergence():
    h = 0.5
    previous_y4 = None
    halverings_count = 0
    
    while True:
        _, y = euler_method(h)
        current_y4 = y[-1]
        
        if previous_y4 is not None:
            diff = abs(current_y4 - previous_y4)
            if diff < 0.0001:  # 1 säker decimal
                return halverings_count, h, current_y4
        
        previous_y4 = current_y4
        h /= 2
        halverings_count += 1
        
        if halverings_count > 20:  # Säkerhetsgräns
            return None, None, None

halveringar, final_h, y4_value = find_convergence()
print(f"\nResultat för konvergensanalys:")
print(f"Antal halveringar: {halveringar}")
print(f"Slutlig steglängd: {final_h}")
print(f"y(4) med felgräns: {y4_value:.6f}")