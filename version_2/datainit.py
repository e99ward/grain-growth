import numpy as np

def GenerateInitGrain(ave, std, size):
    '''
    generatre the grain size data
    '''
    filename = 'd_0000000.txt'
    data = np.random.normal(int(ave), int(std), int(size))
    data.sort()
    # save in numpy format
    np.save(filename, data)
    # save in ascii format
    with open(filename, 'w') as handle:
        i = 0
        for x in data:
            handle.write('{0:.10f} '.format(x))
            i += 1
            if i%10 == 0:
                handle.write('\n')