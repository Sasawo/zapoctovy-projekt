# Šach
# Samuel Lipovský, I. ročník
# zimný semester 2023 / 24
# Programování 1 NPRG030
import tkinter


class Update:

    # Vytvorí grafické rozhranie spolu
    # s tlačidlami na zavretie okna a vzdanie sa
    def __init__(self):

        # Inicializuje grafické rozhranie
        self.root = tkinter.Tk()
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.attributes('-fullscreen', True)
        self.c = tkinter.Canvas(self.root, background='#90afe0', highlightthickness=0, width=self.width, height=self.height)
        self.c.pack()

        # Inicializuje tlačidlo na zavretie okna
        self.close = tkinter.Button(self.root, text='X', width=5, height=1, bd='0', command=self.root.destroy, background='#c71c3e')
        self.close.place(anchor='ne', x=self.width, y=0)

        # Inicializuje tlačidlo na vzdanie sa
        self.resign = tkinter.Button(self.root, text='R E S I G N', font=('Impact', 25), width=10, height=1, bd='0', command=self.resign, background='#4444ef')
        self.resign.place(anchor='center', x=self.width / 10 * 9, y=self.height / 2)
        self.reset(1)

    # Vytvorí vzor šachovnice, začiatočné uloženie figúrok a inicializuje potrebné premenné
    def reset(self, first=None):
        if first is None:
            self.c.delete('all')
            self.end.place(anchor='center', x=-self.width, y=0)
            self.redo.place(anchor='center', x=-self.width, y=0)
            self.resign.place(anchor='center', x=self.width / 10 * 9, y=self.height / 2)

        # Tvorba šachovnice
        for i in range(8):
            for k in range(4):
                self.c.create_rectangle(self.width / 14 * (3 + i % 2 + 2 * k), self.height / 8 * i,
                                        self.width / 14 * (4 + i % 2 + 2 * k), self.height / 8 * (i + 1), fill='#6587f0')
                self.c.create_rectangle(self.width / 14 * (3 + (i + 1) % 2 + 2 * k), self.height / 8 * i,
                                        self.width / 14 * (4 + (i + 1) % 2 + 2 * k), self.height / 8 * (i + 1), fill='#4e76ed')

        # Inicializácia premenných
        self.white, self.black = [8, 16, 129, 36, 66, 255 << 8], [x << 48 for x in [8 << 8, 16 << 8, 129 << 8, 36 << 8, 66 << 8, 255]]
        '''self.white, self.black = [8, 16, 129, 36, 66, 0], [x << 48 for x in [8 << 8, 16 << 8, 129 << 8, 36 << 8, 66 << 8, 0]]'''
        self.whitetaken, self.blacktaken = [], []
        self.whitecastle, self.blackcastle, self.tot = [1, 1], [1, 1], [0, 0]
        for i in self.white:
            self.tot[0] |= i
        for i in self.black:
            self.tot[1] |= i
        self.moves, self.moving, self.movement, self.castling = [], [0, self.white, self.black, 'self.white', 'self.black'], [], []
        self.bounds, self.checked, self.checksave, self.checkblock, self.whiteenpass, self.blackenpass = 9331882296111890817, 0, 0, 0, 0, 0
        self.x, self.y, self.check, self.save, self.checktxt, self.stopdraw = 0, 0, 0, 0, 0, 0

        # Volá funkciu, ktorá generuje figúrky
        self.generate()
        self.c.bind_all('<Button-1>', self.click)
        self.c.mainloop()

    # Táto funkcia generuje vždy, keď je to potrebné, všetky figúrky na šachovnici, zobrané figúrky a nápis o tom kto je na ťahu
    # Tiež volá funkcie, ktoré kontrolujú či je kráľ šachovaný, alebo či nastal Šach Mat, alebo Pat
    def generate(self):

        # Generovanie figúrok na šachovnici
        self.c.delete('figs', 'moves', 'figstake')
        for i in range(8):
            for k in range(8):
                for m in range(6):
                    if self.white[m] & 2**k << i*8 != 0:
                        self.c.create_text(self.width / 14 * (3.5 + k), self.height / 8 * (i + 0.5),
                                           font=('times new roman', 60), text=chr(9812 + m), tags='figs')
                    elif self.black[m] & 2**k << i*8 != 0:
                        self.c.create_text(self.width / 14 * (3.5 + k), self.height / 8 * (i + 0.5),
                                           font=('times new roman', 60), text=chr(9818 + m), tags='figs')

        # Generovanie textu s ťahom
        self.c.create_text(self.width / 10, self.height / 8 * 3.5, text=f'{(self.moving[3][5:]).upper()} MOVING',
                           fill=self.moving[3][5:], font=('Impact', 35), tags='move')

        # Generovanie bielych zobraných figúrok
        o = 0
        for j, i in enumerate(sorted(self.whitetaken)):
            if i == 5:
                self.c.create_text(20 + 23 * (j - o), self.height / 8 * 7 + 50,
                                   font=('times new roman', 27), text=chr(9812 + i), tags='figstake')
            else:
                self.c.create_text(20 + 23 * j, self.height / 8 * 7,
                                   font=('times new roman', 27), text=chr(9812 + i), tags='figstake')
                o += 1

        # Generovanie čiernych zobraných figúrok
        o = 0
        for j, i in enumerate(sorted(self.blacktaken)):
            if i == 5:
                self.c.create_text(20 + 23 * (j - o), self.height / 8 + 50,
                                   font=('times new roman', 27), text=chr(9818 + i), tags='figstake')
            else:
                self.c.create_text(20 + 23 * j, self.height / 8,
                                   font=('times new roman', 27), text=chr(9818 + i), tags='figstake')
                o += 1

        # Funkcia, ktorá kontroluje šach
        self.checkCheck()

        # Funkcia, ktorá kontroluje Pat a Mat
        self.mateCheck()

    # Táto funckia kontroluje, či by ťah kráľa nevyústil v šach, prípadne kam sa môže uhnúť šachu
    def kingCheckMove(self):

        # Udržiavam si potrebnú premennú o šachovanosti, ktorá sa môže pozmeniť počas funkcie
        if self.checksave == 0:
            self.checksave = self.checked

        # Zisťujem či sa hýbe kráľ
        if self.save[1] == 0:

            # Udržiavam premennú, ktorá ukazuje kam sa môžu figúrky mimo kráľa hýbať, aby ukryli kráľa od šachu, ak je akurát šachovaný
            self.holdcheckblock = self.checkblock

            # Tvorím zoznam všetkých ťahov okolo kráľa a zoznam, kam pôjdu tie z políčok, kde by bol kráľ šachovaný
            tempking = [self.moving[1][0] << 1, self.moving[1][0] >> 1, self.moving[1][0] << 7, self.moving[1][0] >> 7,
                        self.moving[1][0] << 8, self.moving[1][0] >> 8, self.moving[1][0] << 9, self.moving[1][0] >> 9]
            tempking2 = []

            # Ak je možné blokovať šach na políčku okolo kráľa, tak políčko symetrické cez kráľa je pre ťah kráľa zakázané
            for i in range(8):
                if tempking[i] & self.checkblock != 0:
                    tempking[i // 2 * 2 + 1 - i % 2] = 0

            # Ak je políčko kam by sa kráľ mohol posunúť šachované, tak je pridané do druhého vytvoreného zoznamu
            for i in range(8):
                if 1 << 64 > tempking[i] > 0:
                    if self.checkCheck(tempking[i]) > 0:
                        tempking2.append(tempking[i])

            if self.checksave != 0:

                # Pridávame ťahy kráľa do šachu k šachovaným políčkam
                for i in tempking2:
                    if i & self.checkblock == 0:
                        self.checkblock ^= i

                # Ak je možné blokovať šach, tak tu invertujeme tie políčka, pretože tam kde je možné blokovať sa kráľ nemôže posunúť
                for i in tempking:
                    if i & self.tot[0] == 0:
                        self.checkblock ^= i

            # V prípade, že kráľ nie je šachovaný, tu vymažeme všetky jeho ťahy, kde by šachovaný bol
            if self.checksave == 0:
                for j, i in enumerate(self.moves):
                    if i[-1][0] in tempking2:
                        self.moves[j][2] = [0, -1]

        # Vraciam udržiavanú premennú o šachovanosti
        self.checked = self.checksave

    # Táto funkcia vracia zmeny funkcie kingCheckMove
    def kingCheckMoveRevert(self):
        self.checksave = 0
        if self.save[1] == 0:
            self.checkblock = self.holdcheckblock

    # Táto funkcia rozhoduje, ktoré ťahy sú legálne, a ktoré nakresliť na šachovnicu pre zvolenú figúrku
    def generateMoves(self, xtracheck=None):

        # Resetuje všetky ťahy a premenné do začiatočného stavu, aby mohli byť generované nanovo
        self.c.delete('moves')
        for_movetake = 0

        # Volá funkciu, ktorá zisťuje, kam sa král môže pohnúť aj v aj mimo šachu
        self.kingCheckMove()

        # Ak je kráľ šachovaný dvomi a viac figúrkami, a nebol na pohyb zvolený kráľ, funkcia pohyby negeneruje
        if self.checksave >= 2 and self.save[1] != 0:
            return

        # Začíname prechádzať všetky možné ťahy pre zvolenú figúrku
        for i in self.moves:
            # Tento IF sa spúšta pri ťahoch, ktoré sú pohyb na prázdne políčko
            if i[0] == 'move':
                run = 0
                for_movetake = 0

                # Tento IF sa spúšťa pri ťahoch, ktoré sú horizontálne, alebo diagonálne, aby nepretiekli na druhú stranu šachovnice
                if i[1] == 'checkBorders':
                    for j, m in enumerate(i[2:]):

                        # Ak je kráľ šachovaný, kontrolujeme tu, či ťah bude kráľa kryť
                        if (self.checksave >= 1 and m[0] & self.checkblock != 0) or self.checksave == 0:

                            # Kontrolujeme či ťah nepretiekol zdola, zhora, alebo či nenarazil na inú figúrku
                            if m[0] & self.tot[0] == 0 and m[0] & self.tot[1] == 0 and 1 << 64 > m[0] > 0:

                                # Ak ťah pretečie, tu sa pohyb ukončí
                                if self.check & self.bounds != 0 and m[0] & self.bounds != 0 and j == 0:
                                    for_movetake = 1
                                    break

                                # Ak sa ťah dotkne strany, nakreslí sa a pohyb sa ukončí
                                elif m[0] & self.bounds != 0:
                                    self.c.create_text(self.width / 14 * (3.5 + (m[1] % 8)), self.height / 8 * (m[1] // 8 + 0.5),
                                                       font=('times new roman', 60), text='X', fill='#4444ef', tags='moves')
                                    if m[0] != 0:
                                        self.movement.append(m[0])
                                    for_movetake = 1
                                    break

                                # Ak ťah na okraj nenarazil, spúšťa sa tento ELSE a pohyb pokračuje
                                else:
                                    self.c.create_text(self.width / 14 * (3.5 + (m[1] % 8)), self.height / 8 * (m[1] // 8 + 0.5),
                                                       font=('times new roman', 60), text='X', fill='#4444ef', tags='moves')
                                    if m[0] != 0:
                                        self.movement.append(m[0])
                                    run = 1

                        # Ak ťah kráľa nekryje, ukončujeme pohyb v prípade, že pretiekol cez okraj šachovnice
                        else:
                            if (self.check & self.bounds != 0 and m[0] & self.bounds != 0 and j == 0) or m[0] & self.bounds != 0:
                                for_movetake = 1
                                break

                # Tento ELSE sa spúšťa ak je pohyb vertikálny, a teda netreba kontrolovať okraje
                else:
                    for m in i[2:]:
                        if (self.checksave == 1 and m[0] & self.checkblock != 0) or self.checksave == 0:

                            # Ukončí pohyb, ak narazí na figúrku
                            if m[0] & self.tot[0] == 0 and m[0] & self.tot[1] == 0:
                                self.c.create_text(self.width / 14 * (3.5 + (m[1] % 8)), self.height / 8 * (m[1] // 8 + 0.5),
                                                   font=('times new roman', 60), text='X', fill='#4444ef', tags='moves')
                                if m[0] != 0:
                                    self.movement.append(m[0])

                            # Ak na figúrku narazí, končíme pohyb
                            else:
                                break

            # Tento ELIF kontroluje, či ťah berie figúrku a nie je na konci dlhšieho pohybu
            elif i[0] == 'take':

                # Tento IF sa spúšťa pri ťahoch, ktoré sú horizontálne, alebo diagonálne, aby nepretiekli na druhú stranu šachovnice
                if i[1] == 'checkBorders':
                    for m in i[2:]:
                        if (self.checksave == 1 and m[0] & self.checkblock != 0) or self.checksave == 0:

                            # Ak ťah pretečie, tu sa pohyb ukončí
                            if self.check & self.bounds != 0 and m[0] & self.bounds != 0 and 1 << 64 > m[0] > 0:
                                break

                            # Ak ťah nepretečie, vykreslí sa tu
                            else:
                                self.c.create_text(self.width / 14 * (3.5 + (m[1] % 8)), self.height / 8 * (m[1] // 8 + 0.5),
                                                   font=('times new roman', 60), text='X', fill='#18d69d', tags='moves')
                                if m[0] != 0:
                                    self.taking.append(m[0])

                # Tento ELSE sa spúšťa ak je pohyb vertikálny, a teda netreba kontrolovať okraje
                else:
                    for m in i[2:]:
                        if (self.checksave == 1 and m[0] & self.checkblock != 0) or self.checksave == 0:
                            self.c.create_text(self.width / 14 * (3.5 + (m[1] % 8)), self.height / 8 * (m[1] // 8 + 0.5),
                                               font=('times new roman', 60), text='X', fill='#18d69d', tags='moves')
                            if m[0] != 0:
                                self.taking.append(m[0])

            # Tento ELIF kontroluje, či ťah berie figúrku na konci sledu pohybov, napr. veža, strelec
            elif i[0] == 'movetake':
                m = i[1]
                if (self.checksave == 1 and m[0] & self.checkblock != 0) or self.checksave == 0:

                    # Tento ELIF sa aktivuje, ak dĺžka sledu pred týmto ťahom je 0
                    if for_movetake == 0:
                        if self.check & self.bounds == 0 or m[0] & self.bounds == 0 or run == 1:
                            self.c.create_text(self.width / 14 * (3.5 + (m[1] % 8)), self.height / 8 * (m[1] // 8 + 0.5),
                                               font=('times new roman', 60), text='X', fill='#18d69d', tags='moves')
                            if m[0] != 0:
                                self.taking.append(m[0])

            # Tento ELIF kontroluje či sa hýbe jazdec, nakoľko potrebuje špeciálne ohraničenie
            elif i[0] == 'knight':

                # Tento IF kontroluje, či by sa pohyb nevykreslil ďalej ako 2 štvorčeky od koňa, teda by pretiekli cez stranu
                if abs(self.x - (i[2][1] % 8)) <= 2 and i[2][0] > 0:
                    m = i[2]
                    if (self.checksave == 1 and m[0] & self.checkblock != 0) or self.checksave == 0:

                        # Tento IF sa aktivuje, ak jazdec berie figúrku
                        if i[1] == 'take':
                            self.c.create_text(self.width / 14 * (3.5 + (m[1] % 8)), self.height / 8 * (m[1] // 8 + 0.5),
                                               font=('times new roman', 60), text='X', fill='#18d69d', tags='moves')
                            if m[0] != 0:
                                self.taking.append(m[0])

                        # Tento IF sa aktivuje, ak jazdec neberie figúrku
                        elif i[1] == 'move':
                            self.c.create_text(self.width / 14 * (3.5 + (m[1] % 8)), self.height / 8 * (m[1] // 8 + 0.5),
                                               font=('times new roman', 60), text='X', fill='#4444ef', tags='moves')
                            if m[0] != 0:
                                self.movement.append(m[0])

            # Tento ELIF kontroluje či je ťah rozšáda
            elif i[0] == 'Castle':
                m = i[1]
                if (self.checksave == 1 and m[0] & self.checkblock != 0) or self.checksave == 0:
                    self.c.create_text(self.width / 14 * (3.5 + (m[1] % 8)), self.height / 8 * (m[1] // 8 + 0.5),
                                       font=('times new roman', 60), text='X', fill='#4444ef', tags='moves')
                    if m[0] != 0:
                        self.castling.append(m[0])

        # Ak bola funkcia zavolaná pri kontrole Patu, vymažú sa vygenerované ťahy
        if xtracheck is not None:
            self.c.delete('moves')

        # Vracia ochranu kráľa do normálu, ak sa práve hýbal kráľ
        self.kingCheckMoveRevert()
        self.checked = self.checktxt

    # Táto funckia generuje všetky pohyby pre zvolenú figúrku
    def movesForBoth(self, xtracheck=None):

        # Tu sa kontroluje, ktorá figúrka bola vybraná
        for i in range(6):
            if self.check & self.moving[1][i] != 0:

                # Ak vybraná figúrka práve blokuje šach, regeneruje sa blokovanie šachu tak, aby sa neuhla
                self.holdcheckblock = self.checkblock
                tempcheck = self.checkCheck(self.moving[1][0])
                self.moving[1][i] ^= self.check
                self.checktxt = self.checked
                if self.moving[1][0] != 0 and self.checkCheck(self.moving[1][0]) > tempcheck:
                    self.checkCheck(None, 1)
                else:
                    self.checkblock = self.holdcheckblock
                self.moving[1][i] ^= self.check
                self.moving[0] = 1

                # Generuje pohyb pre bielych pešiakov
                if i == 5 and self.moving[3] == 'self.white':
                    self.save = [self.check, 5]
                    temp = ['move', 'checkCollision']

                    # Vytvorí pohyb dopredu o 1
                    temp.append([self.check << 8, len(bin(self.check << 8)[2:]) - 1])

                    # Vytvorí pohyb dopredu o 2, ak sa ešte pešiak nehýbal
                    if self.y == 1 and self.check << 8 & self.tot[0] == 0 and self.check << 8 & self.tot[1] == 0:
                        temp.append([self.check << 16, len(bin(self.check << 16)[2:]) - 1])
                    self.moves.append(temp)
                    temp = ['take', 'checkBorders']

                    # Tento IF kontroluje, či môže pešiak brať vľavo
                    if self.check << 7 & self.tot[1] != 0 or (2 ** (self.x - 1) == self.blackenpass and self.y == 4):
                        temp.append([self.check << 7, len(bin(self.check << 7)[2:]) - 1])
                        self.moves.append(temp)
                        temp = ['take', 'checkBorders']

                    # Tento IF kontroluje, či môže pešiak brať vpravo
                    if self.check << 9 & self.tot[1] != 0 or (2 ** (self.x + 1) == self.blackenpass and self.y == 4):
                        temp.append([self.check << 9, len(bin(self.check << 9)[2:]) - 1])
                        self.moves.append(temp)

                # Generuje pohyb pre čiernych pešiakov
                elif i == 5 and self.moving[3] == 'self.black':
                    self.save = [self.check, 5]
                    temp = ['move', 'checkCollision']

                    # Vytvorí pohyb dopredu o 1
                    if self.check >> 8 > 0:
                        temp.append([self.check >> 8, len(bin(self.check >> 8)[2:]) - 1])

                    # Vytvorí pohyb dopredu o 2, ak sa ešte pešiak nehýbal
                    if self.y == 6 and self.check >> 8 & self.tot[0] == 0 and self.check >> 8 & self.tot[1] == 0:
                        temp.append([self.check >> 16, len(bin(self.check >> 16)[2:]) - 1])
                    self.moves.append(temp)
                    temp = ['take', 'checkBorders']

                    # Tento IF kontroluje, či môže pešiak brať vľavo
                    if (self.check >> 7 & self.tot[1] != 0 and self.check >> 7 > 0) or (2 ** (self.x + 1) == self.whiteenpass and self.y == 3):
                        temp.append([self.check >> 7, len(bin(self.check >> 7)[2:]) - 1])
                        self.moves.append(temp)
                        temp = ['take', 'checkBorders']

                    # Tento IF kontroluje, či môže pešiak brať vpravo
                    if (self.check >> 9 & self.tot[1] != 0 and self.check >> 9 > 0) or (2 ** (self.x - 1) == self.whiteenpass and self.y == 3):
                        temp.append([self.check >> 9, len(bin(self.check >> 9)[2:]) - 1])
                        self.moves.append(temp)

                # Generuje pohyb pre jazdcov
                elif i == 4:
                    self.save = [self.check, 4]

                    # Zoznam všetkých pohybov jazdca
                    knightmove = [self.check << 10, self.check << 6, self.check << 17, self.check << 15,
                                  self.check >> 10, self.check >> 6, self.check >> 17, self.check >> 15]

                    # Kontroluje, či ťah jazdca berie figúrku
                    for k in knightmove:
                        if k & self.tot[1] != 0:
                            self.moves.append(['knight', 'take', [k, len(bin(k)[2:]) - 1]])
                        elif k & self.tot[0] == 0:
                            self.moves.append(['knight', 'move', [k, len(bin(k)[2:]) - 1]])

                # Generuje pohyb pre strelcov a kráľovnú
                if i == 3 or i == 1:
                    self.save = [self.check, i]

                    # Vytvára sled ťahov smerom vpravo hore
                    save = self.check >> 7
                    temp = ['move', 'checkBorders']
                    while save & self.tot[0] == 0 and save & self.tot[1] == 0 and save > 0:
                        temp.append([save, len(bin(save)[2:]) - 1])
                        save = save >> 7
                    self.moves.append(temp)

                    # Kontroluje či ťah na konci sledu berie figúrku
                    if save & self.tot[1] != 0:
                        self.moves.append(['movetake', [save, len(bin(save)[2:]) - 1]])

                    # Vytvára sled ťahov smerom vľavo dole
                    save = self.check << 7
                    temp = ['move', 'checkBorders']
                    while save & self.tot[0] == 0 and save & self.tot[1] == 0 and save < 1 << 64:
                        temp.append([save, len(bin(save)[2:]) - 1])
                        save = save << 7
                    self.moves.append(temp)

                    # Kontroluje či ťah na konci sledu berie figúrku
                    if save & self.tot[1] != 0:
                        self.moves.append(['movetake', [save, len(bin(save)[2:]) - 1]])

                    # Vytvára sled ťahov smerom vľavo hore
                    save = self.check >> 9
                    temp = ['move', 'checkBorders']
                    while save & self.tot[0] == 0 and save & self.tot[1] == 0 and save > 0:
                        temp.append([save, len(bin(save)[2:]) - 1])
                        save = save >> 9
                    self.moves.append(temp)

                    # Kontroluje či ťah na konci sledu berie figúrku
                    if save & self.tot[1] != 0:
                        self.moves.append(['movetake', [save, len(bin(save)[2:]) - 1]])

                    # Vytvára sled ťahov smerom vľavo dole
                    save = self.check << 9
                    temp = ['move', 'checkBorders']
                    while save & self.tot[0] == 0 and save & self.tot[1] == 0 and save < 1 << 64:
                        temp.append([save, len(bin(save)[2:]) - 1])
                        save = save << 9
                    self.moves.append(temp)

                    # Kontroluje či ťah na konci sledu berie figúrku
                    if save & self.tot[1] != 0:
                        self.moves.append(['movetake', [save, len(bin(save)[2:]) - 1]])

                # Generuje pohyb pre veže a kráľovnú
                if i == 2 or i == 1:
                    self.save = [self.check, i]
                    save = self.check >> 1
                    temp = ['move', 'checkBorders']

                    # Vytvára sled ťahov smerom vľavo
                    while save & self.tot[0] == 0 and save & self.tot[1] == 0 and save > 0:
                        temp.append([save, len(bin(save)[2:]) - 1])
                        save = save >> 1
                    self.moves.append(temp)

                    # Kontroluje či ťah na konci sledu berie figúrku
                    if save & self.tot[1] != 0:
                        self.moves.append(['movetake', [save, len(bin(save)[2:]) - 1]])
                    save = self.check << 1
                    temp = ['move', 'checkBorders']

                    # Vytvára sled ťahov smerom vpravo
                    while save & self.tot[0] == 0 and save & self.tot[1] == 0 and save < 1 << 64:
                        temp.append([save, len(bin(save)[2:]) - 1])
                        save = save << 1
                    self.moves.append(temp)

                    # Kontroluje či ťah na konci sledu berie figúrku
                    if save & self.tot[1] != 0:
                        self.moves.append(['movetake', [save, len(bin(save)[2:]) - 1]])
                    save = self.check >> 8
                    temp = ['move', 'checkCollision']

                    # Vytvára sled ťahov smerom hore
                    while save & self.tot[0] == 0 and save & self.tot[1] == 0 and save > 0:
                        temp.append([save, len(bin(save)[2:]) - 1])
                        save = save >> 8
                    self.moves.append(temp)

                    # Kontroluje či ťah na konci sledu berie figúrku
                    if save & self.tot[1] != 0:
                        self.moves.append(['take', 'checkCollision', [save, len(bin(save)[2:]) - 1]])
                    save = self.check << 8
                    temp = ['move', 'checkCollision']

                    # Vytvára sled ťahov smerom dole
                    while save & self.tot[0] == 0 and save & self.tot[1] == 0 and save < 1 << 64:
                        temp.append([save, len(bin(save)[2:]) - 1])
                        save = save << 8
                    self.moves.append(temp)

                    # Kontroluje či ťah na konci sledu berie figúrku
                    if save & self.tot[1] != 0:
                        self.moves.append(['take', 'checkCollision', [save, len(bin(save)[2:]) - 1]])

                # Generuje pohyby pre kráľa
                elif i == 0:
                    self.save = [self.check, 0]

                    # Tento IF kontroluje, či má biely kráľ možnú rozšádu
                    if self.moving[3] == 'self.white' and self.checked == 0:

                        # Vytvára malú rozšádu pre bieleho ak je to možné
                        if self.tot[0] & 6 == 0 and self.whitecastle[0] == 1 and self.checkCheck(2) == 0 and self.checkCheck(4) == 0:
                            self.moves.append(['Castle', [2, 1]])

                        # Vytvára veľkú rozšádu pre bieleho ak je to možné
                        if self.tot[0] & 112 == 0 and self.whitecastle[1] == 1 and self.checkCheck(16) == 0 and self.checkCheck(32) == 0:
                            self.moves.append(['Castle', [32, 5]])

                    # Tento ELIF kontroluje, či má čierny kráľ možnú rozšádu
                    elif self.moving[3] == 'self.black' and self.checked == 0:

                        # Vytvára malú rozšádu pre čierneho ak je to možné
                        if (self.tot[0] & 432345564227567616 == 0 and self.blackcastle[0] == 1
                                and self.checkCheck(144115188075855872) == 0 and self.checkCheck(288230376151711744) == 0):
                            self.moves.append(['Castle', [144115188075855872, len(bin(144115188075855872)[2:]) - 1]])

                        # Vytvára veľkú rozšádu pre čierneho ak je to možné
                        if (self.tot[0] & 8070450532247928832 == 0 and self.blackcastle[1] == 1
                                and self.checkCheck(2305843009213693952) == 0 and self.checkCheck(1152921504606846976) == 0):
                            self.moves.append(['Castle', [2305843009213693952, len(bin(2305843009213693952)[2:]) - 1]])

                    # Zoznam všetkých možných ťahov pre kráľa bez rozšád
                    kingmove = [self.check << 1, self.check << 7, self.check << 8, self.check << 9,
                                self.check >> 1, self.check >> 7, self.check >> 8, self.check >> 9]

                    # Kontroluje, či ťah berie figúrku
                    for j, k in enumerate(kingmove):
                        if (k == self.check << 8 or k == self.check >> 8) and 1 << 64 > k > 0:
                            temp = ['take', 'checkCollision']
                        else:
                            temp = ['take', 'checkBorders']
                        if k & self.tot[1] != 0:
                            temp.append([k, len(bin(k)[2:]) - 1])
                            self.moves.append(temp)
                            kingmove[j] = 'nope'

                    # Vytvára všetky ťahy, ktoré figúrku neberú ako ťahy na prázdne políčko
                    for k in kingmove:
                        if (k == self.check << 8 or k == self.check >> 8) and 1 << 64 > k > 0:
                            temp = ['move', 'checkCollision']
                        else:
                            temp = ['move', 'checkBorders']
                        if k != 'nope':
                            temp.append([k, len(bin(k)[2:]) - 1])
                            self.moves.append(temp)

                # Volá funkciu, ktorá skontroluje, ktoré vygenerované ťahy sú legálne a vykreslí ich
                self.generateMoves(xtracheck)

    # Táto funkcia kontroluje či je kráľ (alebo pri kontrolách hociaké políčko) šachovaný
    def checkCheck(self, position=None, xtracheck=None):

        # Regeneruje kontrolu rozostavenia figúrok, tvorí potrebné premenné a
        # zisťuje či ide o šach, alebo len kontrolu a podľa toho rozhodne priebeh funkcie
        self.tot = [0, 0]
        for i in self.moving[1]:
            self.tot[0] |= i
        for i in self.moving[2]:
            self.tot[1] |= i
        if position is not None:
            savepos = 1
            self.flip()
        else:
            savepos = 0
            if xtracheck is None:
                position = self.moving[2][0]
            else:
                self.flip()
                position = self.moving[2][0]
        self.prepking = [position << 1, position >> 1, position >> 7, position << 7,
                         position >> 8, position << 8, position >> 9, position << 9]
        self.checkblock = 0
        checkblockhelp = []
        self.checked = 0
        blockhelphelp = []

        # Pre potrebu kontroly, ak sa parameter xtracheck = 'kingOff', tak sa nekontroluje, či je políčko šachované kráľom
        if xtracheck != 'kingOff':
            for j, i in enumerate(self.prepking):
                if i & self.moving[1][0] != 0:
                    self.checked += 1
                    break

        # Tvorí sled ťahov smerom vpravo dole a kontroluje či na jeho konci je strelec alebo kráľovná
        if position & self.bounds == 0 or position << 9 & self.bounds == 0:
            temp = position << 9
            blockhelphelp.append(temp)
            while temp & self.bounds == 0 and temp & self.tot[0] == 0 and temp & self.tot[1] == 0 and temp < 1 << 64:
                temp = temp << 9
                blockhelphelp.append(temp)
            if temp & self.moving[1][1] != 0 or temp & self.moving[1][3] != 0:
                self.checked += 1
                checkblockhelp.extend(blockhelphelp)

        # Tvorí sled ťahov smerom vpravo a kontroluje či na jeho konci je veža alebo kráľovná
        blockhelphelp = []
        temp = position << 8
        blockhelphelp.append(temp)
        while temp & self.tot[0] == 0 and temp & self.tot[1] == 0 and temp < 1 << 64:
            temp = temp << 8
            blockhelphelp.append(temp)
        if temp & self.moving[1][1] != 0 or temp & self.moving[1][2] != 0:
            self.checked += 1
            checkblockhelp.extend(blockhelphelp)

        # Tvorí sled ťahov smerom vľavo dole a kontroluje či na jeho konci je strelec alebo kráľovná
        blockhelphelp = []
        if position & self.bounds == 0 or position << 7 & self.bounds == 0:
            temp = position << 7
            blockhelphelp.append(temp)
            while temp & self.bounds == 0 and temp & self.tot[0] == 0 and temp & self.tot[1] == 0 and temp < 1 << 64:
                temp = temp << 7
                blockhelphelp.append(temp)
            if temp & self.moving[1][1] != 0 or temp & self.moving[1][3] != 0:
                self.checked += 1
                checkblockhelp.extend(blockhelphelp)

        # Tvorí sled ťahov smerom dole a kontroluje či na jeho konci je veža alebo kráľovná
        blockhelphelp = []
        if position & self.bounds == 0 or position << 1 & self.bounds == 0:
            temp = position << 1
            blockhelphelp.append(temp)
            while temp & self.bounds == 0 and temp & self.tot[0] == 0 and temp & self.tot[1] == 0 and temp < 1 << 64:
                temp = temp << 1
                blockhelphelp.append(temp)
            if temp & self.moving[1][1] != 0 or temp & self.moving[1][2] != 0:
                self.checked += 1
                checkblockhelp.extend(blockhelphelp)

        # Tvorí sled ťahov smerom vľavo hore a kontroluje či na jeho konci je strelec alebo kráľovná
        blockhelphelp = []
        if position & self.bounds == 0 or position >> 9 & self.bounds == 0:
            temp = position >> 9
            blockhelphelp.append(temp)
            while temp & self.bounds == 0 and temp & self.tot[0] == 0 and temp & self.tot[1] == 0 and temp > 0:
                temp = temp >> 9
                blockhelphelp.append(temp)
            if temp & self.moving[1][1] != 0 or temp & self.moving[1][3] != 0:
                self.checked += 1
                checkblockhelp.extend(blockhelphelp)

        # Tvorí sled ťahov smerom hore a kontroluje či na jeho konci je veža alebo kráľovná
        blockhelphelp = []
        temp = position >> 8
        blockhelphelp.append(temp)
        while temp & self.tot[0] == 0 and temp & self.tot[1] == 0 and temp > 0:
            temp = temp >> 8
            blockhelphelp.append(temp)
        if temp & self.moving[1][1] != 0 or temp & self.moving[1][2] != 0:
            self.checked += 1
            checkblockhelp.extend(blockhelphelp)

        # Tvorí sled ťahov smerom vpravo hore a kontroluje či na jeho konci je strelec alebo kráľovná
        blockhelphelp = []
        if position & self.bounds == 0 or position >> 7 & self.bounds == 0:
            temp = position >> 7
            blockhelphelp.append(temp)
            while temp & self.bounds == 0 and temp & self.tot[0] == 0 and temp & self.tot[1] == 0 and temp > 0:
                temp = temp >> 7
                blockhelphelp.append(temp)
            if temp & self.moving[1][1] != 0 or temp & self.moving[1][3] != 0:
                self.checked += 1
                checkblockhelp.extend(blockhelphelp)

        # Tvorí sled ťahov smerom vľavo a kontroluje či na jeho konci je veža alebo kráľovná
        blockhelphelp = []
        if position & self.bounds == 0 or position >> 1 & self.bounds == 0:
            temp = position >> 1
            blockhelphelp.append(temp)
            while temp & self.bounds == 0 and temp & self.tot[0] == 0 and temp & self.tot[1] == 0 and temp > 0:
                temp = temp >> 1
                blockhelphelp.append(temp)
                if temp == 0:
                    exit()
            if temp & self.moving[1][1] != 0 or temp & self.moving[1][2] != 0:
                self.checked += 1
                checkblockhelp.extend(blockhelphelp)

        # Vytvára ťahy pre jazdca z kontrolovanej pozície, pre zisťenie šachu jazdcom
        blockhelphelp = []
        temp = position
        knightcheck = [position << 10, position >> 6, position << 17, position >> 15,
                       position >> 10, position << 6, position >> 17, position << 15]
        for i in range(8):
            knite = bin(temp)[2:]
            knite = knite[::-1][8*i:8*(i+1)]
            if len(knite) < 8:
                knite = knite + '0'*(8-len(knite))

            # Odstraňuje ťahy, ktoré by pretiekli okrajom šachovnice
            for j, k in enumerate(knite):
                if k == '1':
                    if j == 0:
                        knightcheck[4], knightcheck[5], knightcheck[6], knightcheck[7] = 0, 0, 0, 0
                    elif j == 1:
                        knightcheck[4], knightcheck[5] = 0, 0
                    elif j == 6:
                        knightcheck[0], knightcheck[1] = 0, 0
                    elif j == 7:
                        knightcheck[0], knightcheck[1], knightcheck[2], knightcheck[3] = 0, 0, 0, 0
        for k in knightcheck:
            if k & self.moving[1][4] != 0:
                self.checked += 1
                checkblockhelp.append(k)

        if xtracheck != 'kingOff':
            
            # Kontroluje či je čierny kráľ šachovaný bielym pešiakom
            if self.moving[4] == 'self.black':
                if temp >> 7 & self.moving[1][5] != 0 and (temp >> 7 & self.bounds == 0 or temp & self.bounds == 0):
                    self.checked += 1
                    checkblockhelp.append(temp >> 7)
                if temp >> 9 & self.moving[1][5] != 0 and (temp >> 9 & self.bounds == 0 or temp & self.bounds == 0):
                    self.checked += 1
                    checkblockhelp.append(temp >> 9)

            # Kontroluje či je biely kráľ šachovaný čiernym pešiakom
            else:
                if temp << 7 & self.moving[1][5] != 0 and (temp << 7 & self.bounds == 0 or temp & self.bounds == 0):
                    self.checked += 1
                    checkblockhelp.append(temp << 7)
                if temp << 9 & self.moving[1][5] != 0 and (temp << 9 & self.bounds == 0 or temp & self.bounds == 0):
                    self.checked += 1
                    checkblockhelp.append(temp << 9)
        else:
            
            # Kontroluje pri Mate, či vie biely pešiak blokovať šach
            if self.moving[4] == 'self.black':
                if temp >> 8 & self.moving[1][5] != 0:
                    self.checked += 1
                    checkblockhelp.append(temp >> 8)
                if temp >> 16 & self.moving[1][5] != 0 and 1 << 7 < temp < 1 << 16:
                    self.checked += 1
                    checkblockhelp.append(temp >> 16)
            
            # Kontroluje pri Mate, či vie čierny pešiak blokovať šach
            else:
                if temp << 8 & self.moving[1][5] != 0:
                    self.checked += 1
                    checkblockhelp.append(temp << 8)
                if temp << 16 & self.moving[1][5] != 0 and 1 << 47 < temp < 1 << 56:
                    self.checked += 1
                    checkblockhelp.append(temp << 16)


        # Ak bola kontrola spustená pre kráľa, generuje blokovanie šachu
        if savepos == 0:
            for i in checkblockhelp:
                self.checkblock ^= i

        # Pre kontrolu políčka bol na začiatku funkcie premenený ťah, tu je menený naspäť
        if savepos == 1 or xtracheck is not None:
            self.flip()
        return self.checked

    # Táto funkcia kontroluje, ktoré rozšády sú po predošlom ťahu ešte možné
    def castlesCheck(self):

        # Ak sa pohol kráľ, všetky rozšády danej farby sú vypnuté
        if self.save[1] == 0:
            exec(f'{self.moving[3]}castle = [0, 0]')

        # Ak sa pohla pravá veža, vypne sa veľká rozšáda pre danú farbu
        elif self.save[1] == 2 and self.save[0] & 9223372036854775936 != 0:
            exec(f'{self.moving[3]}castle[1] = 0')

        # Ak sa pohla ľavá veža, vypne sa malá rozšáda pre danú farbu
        elif self.save[1] == 2 and self.save[0] & 36028797018963969 != 0:
            exec(f'{self.moving[3]}castle[0] = 0')

    # Táto funkcia kontroluje, či nastala premena pešiaka
    def promotion(self):

        # Tento IF kontroluje, či posledný pohyb vyústil do premeny pešiaka
        if self.check & 18374686479671623935 != 0 and self.save[1] == 5 and abs(self.y - self.store[1]) == 1 and self.moving[0] == 0:
            self.moving[0] = 2

            # Tento IF spracuje premenu pešiaka pre bieleho
            if self.check > 256:
                self.c.create_polygon(self.width / 14 * (4 + self.x), self.height / 8 * (self.y - 4),
                                      self.width / 14 * (3 + self.x), self.height / 8 * (self.y - 4),
                                      self.width / 14 * (3 + self.x), self.height / 8 * (self.y),
                                      self.width / 14 * (3.5 + self.x), self.height / 8 * (self.y + 0.3),
                                      self.width / 14 * (4 + self.x), self.height / 8 * (self.y), fill='#8abcde', tags='promo')
                for i in range(4):
                    self.c.create_text(self.width / 14 * (3.5 + self.x), self.height / 8 * (self.y - 0.5 - i),
                                       font=('times new roman', 60), text=chr(9813 + i), tags='promo')

            # Tento ELSE spracuje premenu pešiaka pre čierneho
            else:
                self.c.create_polygon(self.width / 14 * (4 + self.x), self.height / 8 * (self.y + 5),
                                      self.width / 14 * (3 + self.x), self.height / 8 * (self.y + 5),
                                      self.width / 14 * (3 + self.x), self.height / 8 * (self.y + 1),
                                      self.width / 14 * (3.5 + self.x), self.height / 8 * (self.y + 0.7),
                                      self.width / 14 * (4 + self.x), self.height / 8 * (self.y + 1), fill='#8abcde', tags='promo')
                for i in range(4):
                    self.c.create_text(self.width / 14 * (3.5 + self.x), self.height / 8 * (self.y + 1.5 + i),
                                       font=('times new roman', 60), text=chr(9819 + i), tags='promo')
            return 1
        return 0

    # Táto funkcia kontroluje či nastal Mat alebo Pat
    def mateCheck(self, finish=None):

        # Udržiavam a tvorím potrebné premenné na kontrolu Matu, Patu, a vrátenie potrebných premenných naspäť po kontrole
        done, pat, tot = 1, 1, [0, 0]
        mateking = [self.moving[2][0] << 1, self.moving[2][0] >> 1, self.moving[2][0] >> 7, self.moving[2][0] << 7,
                    self.moving[2][0] >> 8, self.moving[2][0] << 8, self.moving[2][0] >> 9, self.moving[2][0] << 9]
        for i in bin(self.tot[0])[2:]:
            tot[0] += int(i)
        for i in bin(self.tot[1])[2:]:
            tot[1] += int(i)
        checksave = self.checked
        hold = [int(self.moving[2][0]), self.checkblock, self.check, self.save]

        # Kontroluje sa, či je možné uhnúť sa šachu, kvôli Matu
        self.moving[2][0] = 0
        self.flip(0)
        for j, i in enumerate(mateking):
            if (j == 4 or j == 5) or (hold[0] & self.bounds == 0 or i & self.bounds == 0):
                if 1 << 64 > i > 0 and self.tot[0] & i == 0 and self.checkCheck(i) == 0:
                    done = 0
                    break
        self.flip(0)
        self.moving[2][0] = hold[0]
        self.tot[1] = 0
        for i in self.moving[2]:
            self.tot[1] |= i

        # Kontroluje sa či je možné blokovať šach, kvôli Matu
        for j, i in enumerate(bin(hold[1])[2:][::-1]):
            if i == '1' and self.checkCheck(int(i+j*'0', 2), 'kingOff') > 0:
                done = 0
                break

        # Kontroluje sa či má nejaká figúrka hráča možný ťah kvôli Patu
        self.flip(0)
        for j, i in enumerate(bin(self.tot[0])[2:][::-1]):
            if i == '1':
                self.movement, self.taking, self.moves = [], [], []
                self.check = int(str(i)+j*'0', 2)
                self.movesForBoth(1)
                if len(self.movement) + len(self.taking) > 0:
                    pat = 0
                    break
        self.movement, self.taking, self.moves = [], [], []
        self.flip(0)
        self.checkblock, self.check, self.save, self.checked = hold[1], hold[2], hold[3], checksave

        # Zisťuje sa či je na šachovnici málo materálu na Mat, ak áno, spúšťa Pat
        if ((tot[0] == 2 and (self.moving[1][3] != 0 or self.moving[1][4] != 0)) or tot[0] == 1) and (
                (tot[1] == 2 and (self.moving[2][3] != 0 or self.moving[2][4] != 0)) or tot[1] == 1):
            pat = 1

        # Ak sú splnené podmienky na Pat/Mat, vykreslí sa tabuľka ukončenia hry
        if (done == 1 and self.checked > 0) or (pat == 1 and self.checked == 0) or finish == 1:
            self.c.create_rectangle(self.width / 8 * 3, self.height / 4, self.width / 8 * 5, self.height / 4 * 3, fill='black')
            self.end = tkinter.Button(self.root, text='E X I T', font=('Impact', 15),
                                      width=20, height=2, bd='0', command=self.root.destroy, background='#c71c3e')
            self.end.place(anchor='center', x=self.width / 2, y=self.height / 2)
            self.redo = tkinter.Button(self.root, text='R E S E T', font=('Impact', 15),
                                       width=20, height=2, bd='0', command=self.reset, background='#c71c3e')
            self.redo.place(anchor='center', x=self.width / 2, y=self.height / 8 * 5)
            self.stopdraw = 1
            self.resign.place(anchor='center', x=-self.width, y=0)
            self.c.delete('figstake', 'move')

        # Ak sú splnené podmienky na Mat, ukončí sa hra výhrou jedného z hráčov
        if (done == 1 and self.checked > 0) or finish == 1:
            self.c.create_text(self.width / 2, self.height / 3, text=f'{(self.moving[3][5:]).upper()} WINS', fill='white', font=('Impact', 50))

        # Ak sú splnené podmienky na Pat, ukončí sa hra remízou
        elif (pat == 1 and self.checked == 0):
            self.c.create_text(self.width / 2, self.height / 3, text='DRAW', fill='white', font=('Impact', 50))

    # Táto funkcia rieši všetky kliknutia mimo tlačidiel
    def click(self, event):

        # Získavam potrebné premenné z kliknutia a regenerujem premenné o pozíciách figúrok na šachovnici
        self.store = [self.x, self.y, self.check]
        self.tot = [0, 0]
        for i in self.moving[1]:
            self.tot[0] |= i
        for i in self.moving[2]:
            self.tot[1] |= i
        self.x, self.y = (event.x - ((self.width / 14) * 3)) // (self.width / 14), event.y // (self.height / 8)
        self.check = 1 << (int(self.y)*8) << int(self.x)
        if self.x > 7:
            return
        # Tu sa vykonáva premena pešiaka
        if self.moving[0] == 2:
            if self.x == self.store[0] and 0 < abs(self.y - self.store[1]) < 5:
                exec(f'{self.moving[4]}[{int(abs(self.y - self.store[1]))}] = {self.moving[4]}[{int(abs(self.y - self.store[1]))}] ^ ({self.store[2]})')
                exec(f'{self.moving[4]}[5] = {self.moving[4]}[5] ^ ({self.store[2]})')
                self.c.delete('promo')
                self.flip()
                self.generate()
                self.flip()
                self.moving[0] = 3

        # Tu sa vykonáva rozšáda
        if self.moving[0] == 1:

            # Tu sa kontroluje, či je zvolený ťah rozšáda
            for i in self.castling:
                if i & self.check != 0:
                    castglitch = 0

                    # Kontroluje možnosť malej rozšády pre bieleho
                    if i == 2 and self.whitecastle[0] == 1:
                        self.white[0], self.white[2] = self.white[0] ^ 10, self.white[2] ^ 5
                        castglitch = 1

                    # Kontroluje možnosť veľkej rozšády pre bieleho
                    elif i == 32 and self.whitecastle[1] == 1:
                        self.white[0], self.white[2] = self.white[0] ^ 40, self.white[2] ^ 144
                        castglitch = 1

                    # Kontroluje možnosť malej rozšády pre čierneho
                    elif i == 144115188075855872 and self.blackcastle[0] == 1:
                        self.black[0], self.black[2] = self.black[0] ^ 720575940379279360, self.black[2] ^ 360287970189639680
                        castglitch = 1

                    # Kontroluje možnosť veľkej rozšády pre čierneho
                    elif i == 2305843009213693952 and self.blackcastle[1] == 1:
                        self.black[0], self.black[2] = self.black[0] ^ 2882303761517117440, self.black[2] ^ 10376293541461622784
                        castglitch = 1

                    # Ak rozšáda prebehla, táto funkcia ukončí pohyb hráča
                    if castglitch == 1:
                        self.generate()
                        self.castling = []
                        self.moving = [0, self.moving[2], self.moving[1], self.moving[4], self.moving[3]]
                        break
            
            for j, i in enumerate(self.moving[2]):

                # Tento IF kontroluje, či zvolený ťah brania figúrky skutočne berie figúrku
                if i & self.check != 0 or (self.blackenpass << 40 == self.check and j == 5) or (self.whiteenpass << 16 == self.check and j == 5):
                    wait = j
                    for k in self.taking:

                        # Tento IF kontroluje, či zvolený ťah brania figúrky je legálny
                        if self.check & k != 0:

                            # Prevedie branie figúrky
                            if i & self.check != 0:
                                exec(f'{self.moving[4]}[{wait}] = {self.moving[4]}[{wait}] ^ {self.check}')

                            # Prevedie branie figúrky pre en passant
                            elif self.blackenpass << 40 == self.check:
                                exec(f'{self.moving[4]}[{wait}] = {self.moving[4]}[{wait}] ^ {self.check >> 8}')
                            elif self.whiteenpass << 16 == self.check:
                                exec(f'{self.moving[4]}[{wait}] = {self.moving[4]}[{wait}] ^ {self.check << 8}')
                            exec(f'{self.moving[3]}[{self.save[1]}] = {self.moving[3]}[{self.save[1]}] ^ ({self.check} | {self.save[0]})')
                            exec(f'{self.moving[4]}taken.append({wait})')

                            # Skontroluje ktoré rozšády sú ešte možné, vygeneruje nové postavenie na šachovnicu a zmení, kto je na ťahu
                            self.castlesCheck()
                            self.generate()
                            self.flip(0)
                            break

            # Tento IF kontroluje, či zvolený ťah je legálny
            if self.check in self.movement:

                # Ak je ťah legálny, tu sa ťah prevedie
                self.whiteenpass, self.blackenpass = 0, 0
                if self.save[1] == 5 and 2 < self.y < 5 and (self.save[0] < 65536 or self.save[0] > 140737488355328):
                    exec(f'{self.moving[3]}enpass ^= 1 << int(self.x)')
                exec(f'{self.moving[3]}[{self.save[1]}] = {self.moving[3]}[{self.save[1]}] ^ ({self.check} | {self.save[0]})')

                # Skontroluje ktoré rozšády sú ešte možné, vygeneruje nové postavenie na šachovnicu a zmení, kto je na ťahu
                self.castlesCheck()
                self.generate()
                self.flip(0)
                self.movement = []

            # Ak sa nezvolil žiadny z vygenerovaných ťahov, tento ELSE vymaže vykreslené ťahy a prejde do stavu vyberania figúrky
            else:
                self.moves, self.movement = [], []
                self.taking, self.castling = [], []
                self.c.delete('moves')

            # Volá funkciu, ktorá kontroluje, či je možná premena pešiaka
            if self.promotion() == 1:
                return

            # Mení pohybový state na vyberanie figúrky, ak nenasleduje premena pešiaka
            if self.moving[0] < 2:
                self.moving[0] = 0

        # Ak nie je zvolená na ťah žiadna figúrka, spúšťa sa tento IF
        if self.moving[0] == 0:
            self.moves, self.taking = [], []
            self.movesForBoth()

        # Mení pohybový stav na vyberanie figúrky, ak sa práve premenil pešiak
        if self.moving[0] == 3:
            self.moving[0] = 0

        # Vykresľuje text, ktorý notifikuje o tom, ktorý hráč je na ťahu
        self.c.delete('move')
        if self.stopdraw == 0:
            self.c.create_text(self.width / 10, self.height / 8 * 3.5, text=f'{(self.moving[3][5:]).upper()} MOVING',
                               fill=self.moving[3][5:], font=('Impact', 35), tags='move')

            # Vykresľuje text, ktorý notifikuje, že hráč na ťahu je v šachu
            if self.checked > 0:
                self.c.create_text(self.width / 10, self.height / 8 * 4.5, text='IN CHECK', fill=self.moving[3][5:],
                                   font=('Impact', 35), tags='move')

    # Táto funkcia preklápa kto je na ťahu
    def flip(self, zero=None):
        self.tot[0], self.tot[1] = self.tot[1], self.tot[0]
        self.moving = [self.moving[0], self.moving[2], self.moving[1], self.moving[4], self.moving[3]]
        if zero is not None:
            self.moving[0] = zero

    # Táto funckia ukončí hru pri vzdaní sa
    def resign(self):
        self.flip()
        self.mateCheck(1)


# Vytvára inštanciu class, ktorá obsahuje kód hry
chess = Update()
