########################################################
# ------------------------------------------------------#
#
# Machine Perception and Cognitive Robotics Laboratory
#   Center for Complex Systems and Brain Sciences
#           Florida Atlantic University
#
#------------------------------------------------------#
########################################################
#------------------------------------------------------#
#
# Distributed ALVINN, See:
# Pomerleau, Dean A. Alvinn:
# An autonomous land vehicle in a neural network.
# No. AIP-77. Carnegie-Mellon Univ Pittsburgh Pa
# Artificial Intelligence And Psychology Project, 1989.
#
#------------------------------------------------------#
########################################################

from roverShell import *


class roverBrain():
    def __init__(self):
        self.quit = False
        self.rover = roverShell()

        self.fps = 10 # Camera Frame Rate
        self.windowSize = [840, 380]
        self.imageRect = (0, 0, 320, 240)
        self.displayCaption = "Machine Perception and Cognitive Robotics RALVINN"

        pygame.init()
        pygame.display.init()
        pygame.display.set_caption(self.displayCaption)
        self.screen = pygame.display.set_mode(self.windowSize)
        self.clock = pygame.time.Clock()
        self.run()


    def run(self):
        sleep(1.5)
        while not self.quit:
            self.parseControls()
            self.refreshVideo()
        self.rover.quit = True
        pygame.quit()

    def blitscale(self, x):
        x -= np.min(x)
        x = x / np.linalg.norm(x)
        x *= 255.0 / x.max()

        return x


    def refreshVideo(self):

        self.rover.lock.acquire()
        image = self.rover.currentImage
        self.rover.lock.release()

        image = pygame.image.load(cStringIO.StringIO(image), 'tmp.jpg').convert()

        imagearray = pygame.surfarray.array3d(image)
        imagearray = imresize(imagearray, (32, 24))
        image10 = pygame.surfarray.make_surface(imagearray)

        self.screen.blit(image10, (400, 0))
        pygame.display.update((400, 0, 32, 24))

        # in min(7) 7 is the number of neurons you can see.
        for k in range(min(7, self.rover.n2)):
            imagew11 = pygame.surfarray.make_surface(np.reshape(self.blitscale(self.rover.w1[:-1, k]), (32, 24, 3)))
            self.screen.blit(imagew11, (500 + 40 * k, 0))
            pygame.display.update((500 + 40 * k, 0, 32, 24))

        for k in range(min(7, self.rover.n2)):
            imagedw11 = pygame.surfarray.make_surface(np.reshape(self.blitscale(self.rover.dw1[:-1, k]), (32, 24, 3)))
            self.screen.blit(imagedw11, (500 + 40 * k, 50))
            pygame.display.update((500 + 40 * k, 50, 32, 24))

        self.screen.blit(image, (0, 0))
        pygame.display.update(self.imageRect)

        self.clock.tick(self.fps)


    def parseControls(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit = True
            elif event.type == KEYDOWN:
                if event.key in (K_j, K_k, K_SPACE, K_u, K_i, K_o):
                    self.updatePeripherals(event.key)
                elif event.key in (K_w, K_a, K_s, K_d, K_q, K_e, K_z, K_c, K_r):
                    self.updateTreads(event.key)
                else:
                    pass
            elif event.type == KEYUP:
                if event.key in (K_w, K_a, K_s, K_d, K_q, K_e, K_z, K_c, K_r):
                    self.updateTreads()
                elif event.key in (K_j, K_k):
                    self.updatePeripherals()
                else:
                    pass
            else:
                pass


    def updateTreads(self, key=None):

        # tread speed ranges from 0 (none) to one (full speed) so [.5 ,.5] would be half full speed
        if key is None:
            self.rover.treads = [0, 0]
        elif key is K_w:
            self.rover.treads = [1, 1]
        elif key is K_s:
            self.rover.treads = [-1, -1]
        elif key is K_a:
            self.rover.treads = [-1, 1]
        elif key is K_d:
            self.rover.treads = [1, -1]
        elif key is K_q:
            self.rover.treads = [.1, 1]
        elif key is K_e:
            self.rover.treads = [1, .1]
        elif key is K_z:
            self.rover.treads = [-.1, -1]
        elif key is K_c:
            self.rover.treads = [-1, -.1]
        else:
            pass


    def updatePeripherals(self, key=None):
        if key is None:
            self.rover.peripherals['camera'] = 0
        elif key is K_j:
            self.rover.peripherals['camera'] = 1
        elif key is K_k:
            self.rover.peripherals['camera'] = -1
        elif key is K_u:
            self.rover.peripherals['stealth'] = not \
                self.rover.peripherals['stealth']
        elif key is K_i:
            self.rover.peripherals['lights'] = not \
                self.rover.peripherals['lights']
        elif key is K_o:
            self.rover.peripherals['detect'] = not \
                self.rover.peripherals['detect']
        elif key is K_SPACE:
            pass
        else:
            pass