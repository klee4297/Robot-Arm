# Free Sound: https://pgtd.tistory.com/110
# assignment: meet CEO and talk to him.
# assignment: play sound when bounce up

import pygame
import numpy as np
import pygame.font

FPS = 60   # frames per second

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800


def Rmat(degree):
    rad = np.deg2rad(degree) 
    c = np.cos(rad)
    s = np.sin(rad)
    R = np.array([ [c, -s, 0],
                   [s,  c, 0], [0,0,1]])
    return R

def Tmat(tx, ty):
    Translation = np.array( [
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
    return Translation
#

def draw(P, H, screen, color=(100, 200, 200)):
    R = H[:2,:2]
    T = H[:2, 2]
    Ptransformed = P @ R.T + T 
    pygame.draw.polygon(screen, color=color, 
                        points=Ptransformed, width=3)
    return
#


def main():
    pygame.init() # initialize the engine


    screen = pygame.display.set_mode( (WINDOW_WIDTH, WINDOW_HEIGHT) )
    clock = pygame.time.Clock()

    w = 300
    h = 50
    w1=100
    h1=20
    X = np.array([ [0,0], [w, 0], [w, h], [0, h] ])
    X1 = np.array([ [0,0], [w1, 0], [w1, h1], [0, h1] ])
    position = [WINDOW_WIDTH/2, WINDOW_HEIGHT - 50]
    jointangle1 = 0
    jointangle2 = 0
    jointangle3 = 0
    move=0
    
    text_Px=WINDOW_WIDTH - 200
    
    #text
    font = pygame.font.Font(None, 20)
    text1 = font.render("Move base = <- / ->", True, (0, 0, 0))
    text_rect1 = text1.get_rect()
    text_rect1.topleft = (text_Px, WINDOW_HEIGHT -780)
    
    #text2
    text2 = font.render("Move 1st arm = 1 / 2", True, (0, 0, 0))
    text_rect2 = text2.get_rect()
    text_rect2.topleft = (text_Px, WINDOW_HEIGHT -760)
    
    #text3
    text3 = font.render("Move 2nd arm = q / w", True, (0, 0, 0))
    text_rect3 = text3.get_rect()
    text_rect3.topleft = (text_Px, WINDOW_HEIGHT -740)
    
    #text4
    text4 = font.render("Move 3rd arm = a / s", True, (0, 0, 0))
    text_rect4 = text4.get_rect()
    text_rect4.topleft = (text_Px, WINDOW_HEIGHT -720)
    
    #text5
    text5 = font.render("Move gripper = SPACEBAR", True, (0, 0, 0))
    text_rect5 = text5.get_rect()
    text_rect5.topleft = (text_Px, WINDOW_HEIGHT -700)
    

    tick = 0
    done = False
    while not done:
        tick += 1
        #  input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
        keys = pygame.key.get_pressed()

        # drawing
        screen.fill( (208, 219, 136))
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        screen.blit(text3, text_rect3)
        screen.blit(text4, text_rect4)
        screen.blit(text5, text_rect5)
        
        #move joints using keys
        if keys[pygame.K_1]:
            jointangle1 -= 1
        if keys[pygame.K_2]:
            jointangle1 += 1
        if keys[pygame.K_q]:
            jointangle2 -= 1
        if keys[pygame.K_w]:
            jointangle2 += 1
        if keys[pygame.K_a]:
            jointangle3 -= 1
        if keys[pygame.K_s]:
            jointangle3 += 1
            
        #move base using keys
        if keys[pygame.K_LEFT]:
            position[0] -= 3
        if keys[pygame.K_RIGHT]:
            position[0] += 3
            
        #move gripper
        if keys[pygame.K_SPACE]:
            move=15
        elif not keys[pygame.K_ESCAPE]:
            move=0
            
        # base
        pygame.draw.circle(screen, (255,0,0), position, radius=3) 
        H0 = Tmat(position[0], position[1]) @ Tmat(0, -h)
        draw(X, H0, screen, (153,0,153)) # base

        # arm 1
        H1 = H0 @ Tmat(w/2, 0)  
        x, y = H1[0,2], H1[1,2] # joint position
        
        H11 = H1 @ Rmat(-90) @ Rmat(jointangle1) @ Tmat(0, -h/2)
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        draw(X, H11, screen, (0,0, 200)) # arm 1, 90 degree

        # arm 2 255,0,127
        H2 = H11 @ Tmat(w, 0) @ Tmat(0, h/2) # joint 2
        x, y = H2[0,2], H2[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
         
        H21 = H2 @ Rmat(jointangle2) @ Tmat(0, -h/2)
        draw(X, H21, screen, (204,0,102))
        
        # arm 3
        H3 = H21 @ Tmat(w, 0) @ Tmat(0, h/2) # joint 3
        x, y = H3[0,2], H3[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        H31 = H3 @ Rmat(jointangle3) @ Tmat(0, -h/2)
        draw(X, H31, screen, (255,102,178))
        
        # gripper
        G1 = H31 @ Tmat(w, 0) @ Tmat(0, h/2) # joint 4
        x, y = H2[0,2], H2[1,2]
        pygame.draw.circle(screen, (255,0,0), (x,y), radius=3) # joint position
        G11 = G1 @ Rmat(-90) @ Tmat(-w/6, 0)
        draw(X1, G11, screen, (0,0, 200))
        G12 = G11 @ Rmat(-90) @ Tmat(0, 0+move)@ Tmat(-w1, 0)
        draw(X1, G12, screen, (0,0, 200))
        G13 = G11 @ Rmat(-90) @ Tmat(0, w1-h1-move)@ Tmat(-w1, 0)
        draw(X1, G13, screen, (0,0, 200))
        
        #Wheels
        pygame.draw.circle(screen, (153,0,153), (position[0] +50, position[1] ), 35,3)
        pygame.draw.circle(screen, (153,0,153), (position[0] + 250, position[1]), 35,3)
        

        # pygame.draw.circle(screen, RED, (cx, cy), radius=3)
        # finish
        pygame.display.flip()
        clock.tick(FPS)
    # end of while
# end of main()

if __name__ == "__main__":
    main()