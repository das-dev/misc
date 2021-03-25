def display_mult_table(rows):
    for row in range(1, rows+1):
        display_line(row)
    

def display_line(row):
    print(''.join(['{:<4d}'.format(el) for el in calculate_line(row)]))
    

def calculate_line(row):
    return [col * row for col in range(1, row+1)]


display_mult_table(10)

