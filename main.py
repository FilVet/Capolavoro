import turtle
from turtle import Vec2D
from math import tan, radians, sqrt
from progress_bar import show_progress_bar
# Costanti
ITERATION = 17
LENGTH = 1
MODIFIER = sqrt(2)
REAL_LENGTH = None

# Definizione classe segmento
class Segment:
    def __init__(self, A: Vec2D, B: Vec2D) -> None:                                 # Costruttore sapendo 2 vertici
        self.vertex1 = A
        self.vertex2 = B
    def draw(self, t : turtle.Turtle) -> None:                                      # Metodo che disegna il segmento
        t.penup()
        t.setpos(self.vertex1)
        t.pendown()
        t.goto(self.vertex2)
        t.penup()

# Definizione classe retta
class Line:
    def __init__(self, heading_turtle: float, pos_turtle: Vec2D) -> None:           # Costruttore sapendo dove sta guardando la turtle e la sua posizione
        self.point = pos_turtle
        if heading_turtle == 90 or heading_turtle == 270:                           # Guarda verso l'alto, quindi la retta è del tipo x = q
            self.m = float('inf')
            self.q = pos_turtle[0]
        else:                                                                       # Retta del tipo y = mx + q
            self.m = tan(radians(heading_turtle))
            self.q = pos_turtle[1] - self.m*pos_turtle[0]
    

def define_height():                                                                # Funzione che mi prevede quanto l'albero sarà alto
    tot = LENGTH/2
    for i in range(ITERATION):
        tot += LENGTH/2 * (1/MODIFIER) ** (i+1) * (0.5 if i % 2 else 1) ** (i+1)    # Se il numero di iterazioni è pari si arriva alla somma di quelli precedenti * (1 / MODIFIER)^(i+1) * 0.5 ^ (i+1)
                                                                                    # altrimenti alla somma dei precedenti * (1/MODIFIER)^(i+1)
    return tot

def flip_segment (list_of_segment: list[Segment], axis: Line):                      # Funzione che mi specchia un segmento rispetto ad una retta (axis)
    m, q = axis.m, axis.q
    reflected_segment = []
    for segment in list_of_segment:
        A, B = segment.vertex1, segment.vertex2
        if m == float('inf'):                                                       # Caso retta x = q
            new_segment : Segment = Segment (Vec2D(-A[0] + 2*q, A[1]), 
                                           Vec2D(-B[0] + 2*q, B[1]))
        elif m == 0:                                                                # Caso retta y = q
            new_segment : Segment = Segment (Vec2D(A[0], -A[1] + 2*q),
                                           Vec2D(B[0], -B[1] + 2*q))
        else:                                                                       # Caso retta y = mx + q
            m_sq = m ** 2
            m_sq_plus_1 = m_sq + 1
            double_m = 2*m
            new_segment : Segment = Segment (
                Vec2D(((1 - m_sq)*A[0] + double_m*A[1]-double_m*q) / (m_sq_plus_1), 
                      (double_m*A[0] + (m_sq - 1)*A[1] + 2*q) /(m_sq_plus_1)),
                Vec2D(((1 - m_sq)*B[0] + double_m*B[1]-double_m*q) / (m_sq_plus_1), 
                      (double_m*B[0] + (m_sq - 1)*B[1] + 2*q) /(m_sq_plus_1))
                )
        reflected_segment.append(new_segment)
    return list_of_segment + reflected_segment

def draw_tree (t: turtle.Turtle, iter: int, length) -> None:                        # Funzione che mi disegna l'albero
    
    for _ in range(iter):                                                           # Disegno ramo di partenza
        t.forward(length)
        length *= 1/MODIFIER
        t.right(45)
    
    segment_saved : list[Segment] = []                                              # Array con elementi salvati
    for _ in range(iter - 1):                                   
        t.left(45)                                                                  # Procedura per salvare elemento
        vertex1 = t.pos()
        length *= MODIFIER
        t.backward(length)
        segment_saved.append(Segment(vertex1, t.pos()))
        t.left(45)                                                                  # Trovo m della retta che sarà l'asse di simmetria
        segment_saved = flip_segment(segment_saved, Line(t.heading(), t.pos()))     # Specchio segmenti e li salvo
        t.right(45)
        
    length_list = len(segment_saved)
    for index in range(length_list):
        segment_saved[index].draw(t)                                                # Disegno segmenti salvati 
        show_progress_bar(index, length_list)
    show_progress_bar(length_list, length_list)                                     # Evita inprecisione visiva


def set_up_turtle() -> turtle.Turtle:                                               # Funzione che prepara l'ambiente della turtle
    global REAL_LENGTH
    t = turtle.Turtle()
    t.degrees()
    REAL_LENGTH = define_height()
    t.screen.setworldcoordinates(0, 2*REAL_LENGTH, 2*REAL_LENGTH, 0)                # Preparo le dimensioni
    turtle.Screen().setup(1.0, 1.0)
    t.penup()
    turtle.tracer(0, 0)                                                             # Impongo l'aggiornamento manuale del display
    t.setpos(REAL_LENGTH, 2*REAL_LENGTH)                                            # Metto la turtle nella posizione di partenza
    t.write(
        "La turtle sta disegnando, per sapere il progresso guardare il cmd",
        move=False,
        align="center"   
        )
    t.setheading(270)
    t.pendown()
    return t    

if __name__ == "__main__":
    myT = set_up_turtle()                                                           # Creo turtle
    turtle.update()
    myT.clear()
    draw_tree (myT, ITERATION, LENGTH)                                              # Disegno albero
    turtle.update()                                                                 # Aggiorno il display -> faccio vedere l'albero
    myT.penup()
    myT.goto((0, 0))                                                                # Sposto turtle in modo che non dia fastidio
    turtle.update()
    turtle.mainloop()