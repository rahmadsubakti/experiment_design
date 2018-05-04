import numpy as np
from scipy.stats import f

def anova(array):
    array = np.array(array)
    all_sum = array.sum()
    array_size = array.size
    
    square_factor = (all_sum ** 2) / array_size
    total_sum_square = round(((array ** 2).sum() - square_factor), 2)
    
    sum_treatment = []
    for treatment in array:
        a = treatment.sum()
        sum_treatment.append(a)

    sum_treatment = np.array(sum_treatment)

    treatment_sum_square = round((((sum_treatment ** 2).sum() / len(array[0])) - square_factor), 2)
    
    error_sum_square = total_sum_square - treatment_sum_square

    # for anova table

    db_treatment = len(array) - 1
    db_total = array_size - 1
    db_error = db_total - db_treatment

    mid_square_treatment = round(treatment_sum_square / db_treatment, 2)
    mid_square_error = round(error_sum_square / db_error, 2)

    f_calc = round(mid_square_treatment/mid_square_error, 2)

    # f table
    f_95 = round(f.ppf(0.95, db_treatment, db_error), 2)
    f_99 = round(f.ppf(0.99, db_treatment, db_error), 2)

    # generate anova table
    print("DB\tJK\tKT\tF Hitung\t F tabel")
    print('\t\t\t\t\t5%\t1%')
    print('{0}\t{1}\t{2}\t{3}\t\t{4}\t{5}'.format(db_treatment, treatment_sum_square, mid_square_treatment, f_calc, f_95, f_99))
    print('{0}\t{1}\t{2}'.format(db_error, error_sum_square, mid_square_error))
    print('{0}\t{1}'.format(db_total, total_sum_square))

    
# test
anova(array=[
    [8.0, 8.1, 7.5, 7.7],
    [8.3, 8.2, 8.3, 7.9],
    [8.9, 8.1, 8.3, 8.0],
    [9.3, 9.0, 8.2, 8.7],
    [9.7, 9.0, 8.8, 9.0],
    [9.5, 8.9, 8.5, 8.9]
])
