from algorithms.auxiliary_functions import Context
import pygame

def generator(algorithms: list[callable], data_list: list[Context]):
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for data in data_list:
                        for row in data.grid:
                            for cell in row:
                                cell._update_neighbors(data.grid)
                
                    for algorithm, data in zip(algorithms, data_list):
                        algorithm(data)
                        
                if event.key == pygame.K_c:
                    for data in data_list:
                        data.regenerate()

        for data in data_list:
            data.draw()

        pygame.display.update()
        pygame.time.Clock().tick(10)

    pygame.quit()