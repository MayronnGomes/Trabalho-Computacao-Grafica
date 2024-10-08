import CONSTS
import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Time import *
from Formation import *
from Bola import *
from Campo import *
from Triangule import *
from Placar import *
from Util import *

class Game:

    def __init__(self):

        glutInit()
        glutInitDisplayMode(GLUT_MULTISAMPLE | GLUT_DOUBLE | GLUT_RGB)
        glutInitWindowSize(CONSTS.janelaLar, CONSTS.janelaAlt)
        glutInitWindowPosition(0,0)
        glutCreateWindow('FullScreen')
        self.inicio()
        glutTimerFunc(int(1000/CONSTS.FPS), self.timer, 0)      
        glutFullScreen()
        glutKeyboardFunc(self.tecladoASCII)
        glutSpecialFunc(self.tecladoEspecial)
        glutSpecialUpFunc(self.tecladoEspecialUp)
        glutReshapeFunc(self.reshape)
        glutDisplayFunc(self.desenha)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)
        glutMainLoop()

    def inicio(self):
        glClearColor(0, 0.3, 0, 1)
        glLineWidth(5)
        glEnable(GL_MULTISAMPLE)                    
        glEnable(GL_TEXTURE_2D)                      
        glEnable(GL_BLEND);                         
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        CONSTS.texCampo = carregaTextura('../Texturas/campo.jpg')
        CONSTS.texBola = carregaTextura('../Texturas/bola.png')
        CONSTS.texProgBar = carregaTextura('../Texturas/arrow.png')
        CONSTS.texGol = carregaTextura('../Texturas/trave.png') 

        for i in CONSTS.TIME:
            CONSTS.TIME[i] = carregaTextura(f'../Texturas/TIMES PNG/{i}.png')
            CONSTS.SIGLAS[i] = carregaTextura(f'../Texturas/Siglas/{i}.png')

        for i in range(0, 6):
            CONSTS.PLACAR[f'{i}'] = carregaTextura(f'../Texturas/Placar/{i}.png')
        
        for i in CONSTS.TELAS.keys():
            CONSTS.TELAS[i] = carregaTextura(f'../Texturas/Telas/{i}.png')        

        self.campo = Campo(CONSTS.campoLar, CONSTS.campoAlt)
        self.bola = Bola(CONSTS.bolaRaio)
        self.formation = Formation()
        self.nomeA = ''
        self.nomeB = ''
        self.timeA = None
        self.timeB = None
        self.placar = None
        self.option = 0
        self.optionTimeA = 0
        self.optionTimeB = 0
        self.tela = "inicial"

    def desenha(self):
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-CONSTS.mundoLar, CONSTS.mundoLar, -CONSTS.mundoAlt, CONSTS.mundoAlt, -1, 1)

        if self.tela == "inicial":
            cube = Cube()
            triangule = Triangle()

            glPushMatrix()
            glTranslatef(-CONSTS.mundoLar, -CONSTS.mundoAlt, 0)
            glScalef(2 * CONSTS.mundoLar, 2 * CONSTS.mundoAlt, 1)
            glBindTexture(GL_TEXTURE_2D, CONSTS.TELAS[self.tela])
            cube.desenha(True)
            glBindTexture(GL_TEXTURE_2D, 0)
            glPopMatrix()

            glPushMatrix()
            glTranslatef(CONSTS.OPTIONS[self.option].x, CONSTS.OPTIONS[self.option].y, CONSTS.OPTIONS[self.option].z)
            glRotatef(135, 0, 0, 1)
            triangule.desenha(True)
            glPopMatrix()
            
        elif self.tela == "times":
            cube = Cube()
            triangule = Triangle()

            glPushMatrix() # tela
            glTranslatef(-CONSTS.mundoLar, -CONSTS.mundoAlt, 0)
            glScalef(2 * CONSTS.mundoLar, 2 * CONSTS.mundoAlt, 1)
            glBindTexture(GL_TEXTURE_2D, CONSTS.TELAS[self.tela])
            cube.desenha(True)
            glBindTexture(GL_TEXTURE_2D, 0)
            glPopMatrix()

            glPushMatrix() # Seleção
            if self.nomeA != "":
                glScalef(-1, 1, 1)

            glTranslatef(-12.35, 0, 0)
            
            glPushMatrix()
            glTranslatef(CONSTS.OPTIONS[self.option].x, CONSTS.OPTIONS[self.option].y, CONSTS.OPTIONS[self.option].z)
            glRotatef(135, 0, 0, 1)
            triangule.desenha(True)
            glPopMatrix()
            
            glPushMatrix()
            glScale(-1, 1, 1)
            glTranslatef(CONSTS.OPTIONS[self.option].x, CONSTS.OPTIONS[self.option].y, CONSTS.OPTIONS[self.option].z)
            glRotatef(135, 0, 0, 1)
            triangule.desenha(True)
            glPopMatrix()
            glPopMatrix()

            glPushMatrix() # time esquerdo
            glTranslatef(-CONSTS.mundoLar * 0.72, -3, 0)
            glScalef(6, 6, 1)
            glBindTexture(GL_TEXTURE_2D, CONSTS.TIME[CONSTS.OPTIONSTIMES[self.optionTimeA]])
            cube.desenha(True)
            glBindTexture(GL_TEXTURE_2D, 0)
            glPopMatrix()
            
            glPushMatrix() # time direito
            glScalef(-1, 1, 1)
            glTranslatef(-CONSTS.mundoLar * 0.72, -3, 0)
            glScalef(6, 6, 1)
            glBindTexture(GL_TEXTURE_2D, CONSTS.TIME[CONSTS.OPTIONSTIMES[self.optionTimeB]])
            cube.desenha(True)
            glBindTexture(GL_TEXTURE_2D, 0)
            glPopMatrix()

            glPushMatrix() # nome time esquerdo
            glTranslatef(-CONSTS.mundoLar * 0.65, 5.35, 0)
            glScalef(3.2, 1.8, 1)
            glBindTexture(GL_TEXTURE_2D, CONSTS.SIGLAS[CONSTS.OPTIONSTIMES[self.optionTimeA]])
            cube.desenha(True)
            glBindTexture(GL_TEXTURE_2D, 0)
            glPopMatrix()
            
            glPushMatrix() # nome time direito
            glScalef(-1, 1, 1)
            glTranslatef(-CONSTS.mundoLar * 0.65, 5.35, 0)
            glScalef(3.2, 1.8, 1)
            glBindTexture(GL_TEXTURE_2D, CONSTS.SIGLAS[CONSTS.OPTIONSTIMES[self.optionTimeB]])
            cube.desenha(True, invertido=True)
            glBindTexture(GL_TEXTURE_2D, 0)
            glPopMatrix()

            # escolhendo - escolhido

        elif self.tela == "formação1" or self.tela == "formação2":
            self.formation.desenha(self.tela)

        elif self.tela == "jogo":

            glPushMatrix()
            glTranslatef(-(self.campo.largura/2), -(self.campo.altura/2), 0)
            self.campo.desenha()
            self.campo.desenha_gol()

            glPushMatrix()
            glTranslatef(self.campo.largura/2, self.campo.altura/2, 0)
            
            glPushMatrix()
            glTranslatef(-self.bola.raio/2, -self.bola.raio/2, 0)
            glTranslatef(self.bola.pos.x, self.bola.pos.y, self.bola.pos.z)
            glScalef(self.bola.raio, self.bola.raio, 1)
            self.bola.desenha()
            glPopMatrix()

            self.timeA.desenha()
            self.timeB.desenha()

            glPopMatrix()
            glPopMatrix()

            if(CONSTS.progressbar):
                self.bola.desenha_progressbar()

            self.placar.desenha()

        glutSwapBuffers()

    def reshape(self, w, h):
        CONSTS.janelaLar = w
        CONSTS.janelaAlt = h
        CONSTS.mundoLar  = CONSTS.mundoAlt*w/h
        glViewport(0,0,w,h) 

    def timer(self, v):
        glutTimerFunc(int(1000/CONSTS.FPS), self.timer, 0)

        if CONSTS.mov:

            # movimento da bola parou
            if (abs(CONSTS.deslocamento.x + CONSTS.velocidade.x) > abs(CONSTS.forca.x) or abs(CONSTS.deslocamento.y + CONSTS.velocidade.y) > abs(CONSTS.forca.y)):
                
                print('Movimento parou')
                self.gameover()

            # tratamento de colisão e movimento da bola
            else:

                if self.campo.colisao_gol(self.bola, self.placar):
                    self.gameover()
                    self.bola.pos = glm.vec3(0, 0, 0)
                    self.timeA.alterarFormacao()
                    self.timeB.alterarFormacao()

                    if self.vencedor(self.placar):
                        # self.desenha(winner) # desenha uma mensagem de vencedor
                        print(f'vencedor {CONSTS.winner}') 

                elif self.campo.verifica_colisao(self.bola): # colisão no campo
                    recalcMov(CONSTS.normal)
                elif self.bola.pos.x < 0 and self.timeA.colisao(self.bola): # colisão time A
                    recalcMov(CONSTS.normal)
                elif self.bola.pos.x > 0 and self.timeB.colisao(self.bola): # colisão time B
                    recalcMov(CONSTS.normal)

                self.bola.move()

        glutPostRedisplay()

    def mouse(self, button, state, x, y):

        model_view = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)

        win_x = float(x)
        win_y = float(viewport[3] - y)
        win_z = 0.0

        normalized_x, normalized_y, _ = gluUnProject(win_x, win_y, win_z, model_view, projection, viewport)
        normalized_x = round(normalized_x, 3)
        normalized_y = round(normalized_y, 3)

        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            if (self.bola.pos.x - CONSTS.bolaRaio) <= normalized_x <= (self.bola.pos.x + CONSTS.bolaRaio) and (self.bola.pos.y - CONSTS.bolaRaio) <= normalized_y <= (self.bola.pos.y + CONSTS.bolaRaio) and not CONSTS.mov:
                CONSTS.progressbar = True
                CONSTS.forca.x = normalized_x - self.bola.pos.x
                CONSTS.forca.y = normalized_y - self.bola.pos.y
                CONSTS.angleProgressbar = math.degrees(math.atan2(CONSTS.forca.y, CONSTS.forca.x))

        elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            CONSTS.progressbar = False
            if (abs(CONSTS.forca.x) > 0 or abs(CONSTS.forca.y) > 0 or abs(CONSTS.forca.z) > 0) and not CONSTS.mov:
                CONSTS.mov = True
                CONSTS.forca *= -1
                CONSTS.velocidade = glm.normalize(CONSTS.forca) * 0.2
    
    def motion(self, x, y):

        if CONSTS.progressbar:
            
            model_view = glGetDoublev(GL_MODELVIEW_MATRIX)
            projection = glGetDoublev(GL_PROJECTION_MATRIX)
            viewport = glGetIntegerv(GL_VIEWPORT)

            win_x = float(x)
            win_y = float(viewport[3] - y)  # Inverte a coordenada Y da janela
            win_z = 0.0  # Para 2D, a profundidade é geralmente 0

            normalized_x, normalized_y, _ = gluUnProject(win_x, win_y, win_z, model_view, projection, viewport)
            normalized_x = round(normalized_x, 3)
            normalized_y = round(normalized_y, 3)
            CONSTS.forca.x = normalized_x - self.bola.pos.x
            CONSTS.forca.y = normalized_y - self.bola.pos.y
            CONSTS.angleProgressbar = math.degrees(math.atan2(CONSTS.forca.y, CONSTS.forca.x))

    def tecladoASCII(self, key, x, y):
        if key == b'\r':
            if self.tela == "inicial":
                if self.option == 0:
                    self.tela = "times"
                    self.option = 3
                elif self.option == 1:
                    print("options")
                elif self.option == 2:
                    glutLeaveMainLoop()
            elif self.tela == "times":
                if self.nomeA == "":
                    self.nomeA = CONSTS.OPTIONSTIMES[self.optionTimeA]
                    self.timeA = Time(self.nomeA, CONSTS.FORMATION['1'], False)
                else:
                    self.nomeB = CONSTS.OPTIONSTIMES[self.optionTimeB]
                    self.timeB = Time(self.nomeB, CONSTS.FORMATION['1'], True)
                    self.placar = Placar(self.nomeA, self.nomeB)
                    self.tela = "jogo"
            elif self.tela == "formação1":
                self.timeA.formacao = CONSTS.FORMATION[str(self.formation.option)]
                self.tela = "formação2"
            elif self.tela == "formação2":
                self.timeB.formacao = CONSTS.FORMATION[str(self.formation.option)]
                self.tela = "jogo"
        elif key.lower() == b'f' and self.tela == "jogo":
            self.tela = "formação1"
            glutPostRedisplay()
        elif key.lower() == b'q':
            if self.tela == "formação1":
                self.tela = "formação2"
                glutPostRedisplay()
            elif self.tela == "formação2":
                self.tela = "jogo"
                glutPostRedisplay()

    def tecladoEspecial(self, key, x, y):
        if self.tela == "inicial":
            if key == GLUT_KEY_DOWN:
                self.option += 1 if self.option < 2 else 0
            elif key == GLUT_KEY_UP:
                self.option -= 1 if self.option > 0 else 0
        elif self.tela == "times":
            if self.nomeA == "":
                if key == GLUT_KEY_RIGHT:
                    self.optionTimeA += 1 if self.optionTimeA < (len(CONSTS.OPTIONSTIMES) - 1) else 0
                elif key == GLUT_KEY_LEFT:
                    self.optionTimeA -= 1 if self.optionTimeA > 0 else 0
            else:
                if key == GLUT_KEY_RIGHT:
                    self.optionTimeB += 1 if self.optionTimeB < (len(CONSTS.OPTIONSTIMES) - 1) else 0
                elif key == GLUT_KEY_LEFT:
                    self.optionTimeB -= 1 if self.optionTimeB > 0 else 0
        elif self.tela == "formação1" or self.tela == "formação2":
            if key == GLUT_KEY_RIGHT:
                self.formation.option += 1 if self.formation.option < 8 else 0
            elif key == GLUT_KEY_LEFT:
                self.formation.option -= 1 if self.formation.option > 1 else 0
            elif key == GLUT_KEY_DOWN:
                self.formation.option += 4 if self.formation.option < 5 else 0
            elif key == GLUT_KEY_UP:
                self.formation.option -= 4 if self.formation.option > 4 else 0
         
    def tecladoEspecialUp(self, key, x, y):
        if (key == GLUT_KEY_DOWN or key == GLUT_KEY_UP) and self.tela == "inicial":
            glutPostRedisplay()
        elif (key == GLUT_KEY_RIGHT or key == GLUT_KEY_LEFT) and self.tela == "times":
            glutPostRedisplay()
        elif (key == GLUT_KEY_RIGHT or key == GLUT_KEY_LEFT or key == GLUT_KEY_DOWN or key == GLUT_KEY_UP) and (self.tela == "formação1" or self.tela == "formação2"):
            glutPostRedisplay()

    def vencedor(self, placar):
        if placar.score1 == 5:
            CONSTS.winner = placar.time1
            return True
        elif placar.score2 == 5:
            CONSTS.winner = placar.time2
            return True
        else:
            return False

    def gameover(self):

        CONSTS.mov = False
        CONSTS.forca.x = CONSTS.forca.y = CONSTS.forca.z = 0
        CONSTS.deslocamento.x = CONSTS.deslocamento.y = CONSTS.deslocamento.z = 0
        CONSTS.velocidade.x = CONSTS.velocidade.y = CONSTS.velocidade.z = 0
        CONSTS.angleProgressbar = 0.0

if __name__ == "__main__":
    game = Game()
