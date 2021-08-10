import pygame
import random
import tkinter
from tkinter import messagebox

class Kostka_weza:
    rzedy = 20

    def __init__(self, pozycja, ruchX = 1, ruchY = 0, kolor = (0, 100, 0)):
        self.pozycja = pozycja
        self.ruchX = ruchX
        self.ruchY = ruchY
        self.kolor = kolor

    def rysuj_kostke(self, rozmiar, oczy = False):
        dl_kostki = szerokosc // rzedy

        #wspolrzedne dla siatki
        wspX = self.pozycja[0]
        wspY = self.pozycja[1]
        pygame.draw.rect(rozmiar, self.kolor, (wspX * dl_kostki + 1, wspY * dl_kostki + 1, dl_kostki - 2, dl_kostki -2))

        if oczy:
            srodek = dl_kostki // 2
            r = 3
            srodek_oka = (wspX * dl_kostki + srodek - r - 2, wspY * dl_kostki + 8)
            srodek_oka2 = (wspX * dl_kostki + dl_kostki - r * 2, wspY * dl_kostki + 8)
            pygame.draw.circle(rozmiar, (0, 0, 0), srodek_oka, r)
            pygame.draw.circle(rozmiar, (0, 0, 0), srodek_oka2, r)

    def ruchy(self, ruchX, ruchY):
        self.ruchX = ruchX
        self.ruchY = ruchY
        self.pozycja = (self.pozycja[0] + self.ruchX, self.pozycja[1] + self.ruchY)

class Waz:
    cialo_weza = []
    punkt_stacjonarny = {}

    def __init__(self, kolor, pozycja):
        self.color = kolor
        self.glowa = Kostka_weza(pozycja)
        self.ruchX = 1
        self.ruchY = 0
        self.cialo_weza.append(self.glowa)

    def jedzenie(self):
        tail = self.cialo_weza[-1]
        dx, dy = tail.ruchX, tail.ruchY

        #kierunek prawo
        if dx == 1 and dy == 0:
            self.cialo_weza.append(Kostka_weza((tail.pozycja[0] - 1, tail.pozycja[1])))

        #kierunek lewo
        elif dx == -1 and dy == 0:
            self.cialo_weza.append(Kostka_weza((tail.pozycja[0] + 1, tail.pozycja[1])))

        #kierunek dol
        elif dx == 0 and dy == 1:
            self.cialo_weza.append(Kostka_weza((tail.pozycja[0], tail.pozycja[1] - 1)))

        #kierunek gora
        elif dx == 0 and dy == -1:
            self.cialo_weza.append(Kostka_weza((tail.pozycja[0], tail.pozycja[1] + 1)))

        #przypisanie jako nowy ruch
        self.cialo_weza[-1].ruchX = dx
        self.cialo_weza[-1].ruchY = dy


    def poruszanie(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            ruch = pygame.key.get_pressed()

            #lewo
            if ruch[pygame.K_LEFT]:
                self.ruchX = -1
                self.ruchY = 0
                self.punkt_stacjonarny[self.glowa.pozycja[:]] = [self.ruchX, self.ruchY]

            #prawo
            elif ruch[pygame.K_RIGHT]:
                self.ruchX = 1
                self.ruchY = 0
                self.punkt_stacjonarny[self.glowa.pozycja[:]] = [self.ruchX, self.ruchY]

            #gora
            elif ruch[pygame.K_UP]:
                self.ruchY = -1
                self.ruchX = 0
                self.punkt_stacjonarny[self.glowa.pozycja[:]] = [self.ruchX, self.ruchY]

            #dol
            elif ruch[pygame.K_DOWN]:
                self.ruchY = 1
                self.ruchX = 0
                self.punkt_stacjonarny[self.glowa.pozycja[:]] = [self.ruchX, self.ruchY]

        #poruszanie sie reszty ciala weza
        for i, k in enumerate(self.cialo_weza):
            p = k.pozycja[:]
            if p in self.punkt_stacjonarny:
                turn = self.punkt_stacjonarny[p]
                k.ruchy(turn[0], turn[1])
                if i == len(self.cialo_weza) - 1:
                    self.punkt_stacjonarny.pop(p)
            else:
                if k.ruchX == -1 and k.pozycja[0] <= 0:
                    k.pozycja = (k.rzedy - 1, k.pozycja[1])
                elif k.ruchX == 1 and k.pozycja[0] >= k.rzedy - 1:
                    k.pozycja = (0, k.pozycja[1])
                elif k.ruchY == 1 and k.pozycja[1] >= k.rzedy - 1:
                    k.pozycja = (k.pozycja[0], 0)
                elif k.ruchY == -1 and k.pozycja[1] <= 0:
                    k.pozycja = (k.pozycja[0], k.rzedy - 1)
                else:
                    k.ruchy(k.ruchX, k.ruchY)



    def nowy_waz(self):
        for i in range(len(self.cialo_weza) - 1):
            self.cialo_weza.pop()



    def rysuj_weza(self, rozmiar):
        for i, c in enumerate(self.cialo_weza):
            if i == 0:
                c.rysuj_kostke(rozmiar, oczy = True)
            else:
                c.rysuj_kostke(rozmiar)


def rysuj_siatke(szerokosc, rzedy, rozmiar):
    szerokosc_siatki = szerokosc // rzedy

    x = 0
    y = 0
    for i in range(rzedy):
        x = x + szerokosc_siatki
        y = y + szerokosc_siatki
        pygame.draw.line(rozmiar, (173, 255, 47), (x, 0), (x, szerokosc))
        pygame.draw.line(rozmiar, (173, 255, 47), (0, y), (szerokosc, y))


def rysuj_okno(rozmiar):
    rozmiar.fill((0, 191, 255))
    rysuj_siatke(szerokosc, rzedy, rozmiar)
    w.rysuj_weza(rozmiar)
    j.rysuj_kostke(rozmiar)
    pygame.display.update()

def jablko(Waz):
    zajete = Waz.cialo_weza

    while True:
        x = random.randrange(rzedy)
        y = random.randrange(rzedy)
        if len(list(filter(lambda z: z.pozycja == (x,y), zajete))) > 0:
            continue
        else:
            break
    return (x, y)

def message_box(temat, tresc):
    root = tkinter.Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
    messagebox.showinfo(temat, tresc)

    try:
        root.destroy()
    except:
        pass

pygame.display.set_caption('Snake')

def main():
    global szerokosc, wysokosc, rzedy, w, j
    #obszar gry
    szerokosc = 500
    wysokosc = 500
    rzedy = 20

    okno = pygame.display.set_mode((szerokosc, wysokosc))
    w = Waz((0, 100, 0), (10, 10))
    j = Kostka_weza(jablko(w), 0, 0, (255, 0, 0))
    gra = True
    clock = pygame.time.Clock()

    while gra:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gra = False


        pygame.time.delay(50)
        clock.tick(10)
        w.poruszanie()
        if w.glowa.pozycja == j.pozycja:
            w.jedzenie()
            j = Kostka_weza(jablko(w), 0, 0, (255, 0, 0))

        if len(w.cialo_weza) > 1:
            for x in range(1, len(w.cialo_weza)):
                if w.cialo_weza[x].pozycja == w.glowa.pozycja:
                    message_box('Koniec gry', 'Czy chcesz zagrac ponownie?')
                    w.nowy_waz()
                    break

        rysuj_okno(okno)

main()