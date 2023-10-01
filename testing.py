if __name__ == '__main__':
    
    # function: (x(point_one) + (x(point_two) - x(point_one)) /
    # (num), y(point_one) + (y(point_two) - y(point_one)) / (num))

    # C_{1}=(x(B_{1})+(x(O)-x(B_{1}))/(8),y(B_{1})+(y(O)-y(B_{1}))/(8))
    
    def f_text():

        ls1 = ['J_1', 'K_1', 'L_1', 'M_1', 'N_1', 'O_1']
        ls2 = ['I_1', 'J_1', 'K_1', 'L_1', 'M_1', 'N_1']
        ls3 = ['H', 'G', 'F', 'E', 'D', 'C']
        nums = ['15', '16', '17', '18', '19', '20']

        for k, v in enumerate(ls1):
            print(v + ' = (x(' + ls2[k] + ') + (x(' + ls3[k] + ') - x(' + ls2[k] + ')) / (' +
                  nums[k] + '), y(' + ls2[k] + ') + (y(' + ls3[k] + ') - y(' + ls2[k] + ')) / (' + nums[k] + '))')

        
    f_text()
