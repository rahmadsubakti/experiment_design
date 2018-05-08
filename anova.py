import numpy as np
from scipy.stats import f

class Anova:
    """
    Anova(array) -> Anova.anova class

    Generate anova table for one-way test.
    The test should be commit if:
    1. Array must be distributed normally (You can test it with normality test eg. Shapiro-Wilk)
    2. Array is homogen (You can test it with homogeneity test eg. Bartlett test)
    """
    def __init__(self, array, block=False):
        """
        Initial method contain array, total all values of array, size of array, \
        and number of repeat of treatment(it's r)
        """
        # change into numpy array-type
        array = np.array(array)
        self.array = array
        self.all_sum = array.sum()
        self.array_size = array.size
        self.treatment, self.r = array.shape # r represent for repeats or blocks
        self.block = block # value is either True or False

    def db_index(self):
        """ return (db_treatment, db_total, db_error)
        if block=True, return (db_block, db_treatment, db_total, db_error)"""
        db_treatment = len(self.array) - 1
        db_total = self.array_size - 1
        if self.block:
            db_block = self.r - 1
        else:
            db_block = 0

        db_error = db_total - db_treatment - db_block

        if self.block:
            return (db_treatment, db_total, db_error, db_block)

        return (db_treatment, db_total, db_error)

    def square_factor(self):
        """
        return square factor of array
        """
        return (self.all_sum ** 2) / self.array_size

    def sum_square_total(self):
        """
        return sum square of total all values of array
        """
        return round(((self.array ** 2).sum() - self.square_factor()), 2)

    def sum_square_block(self):
        """
        return sum square of blocks if the block=True
        """
        # transpose array
        if self.block:
            transpose_arr = self.array.T
            sum_blocks = transpose_arr.sum(axis=1)
            sum_square = round(((sum_blocks ** 2).sum() / self.treatment) - self.square_factor(), 2)
            
            return sum_square

        return "Your data is not set to block design, it maybe set to complete design"
        
    def sum_square_treatment(self):
        """
        return sum square of treatments
        """
        sum_treatment = []
        for treatment in self.array:
            a = treatment.sum()
            sum_treatment.append(a)

        # change into numpy array-type
        sum_treatment = np.array(sum_treatment)
        return round((((sum_treatment ** 2).sum() / self.r) - self.square_factor()), 2)
    
    def sum_square_error(self):
        """
        return sum square of error
        """
        if self.block:
            return round(self.sum_square_total() - self.sum_square_block() - self.sum_square_treatment(), 2)

        return self.sum_square_total() - self.sum_square_treatment()

    def mid_square_block(self):
        """
        return middle square of sum_square_block()
        """
        if self.block:
            mid_square_block_ = round(self.sum_square_block() / self.db_index()[3], 2)
            return mid_square_block_
        else:
            return "Your data is not set to block design, it maybe set to complete design"

    def mid_square_treatment(self):
        """
        return middle square of sum_square_treatment()
        """
        mid_square_treatment_ = round(self.sum_square_treatment() / self.db_index()[0], 2)
        return mid_square_treatment_

    def mid_square_error(self):
        """
        return middle square of sum_square_error()
        """
        return round(self.sum_square_error() / self.db_index()[2], 2)

    def f_calc(self):
        """
        return F calculated of array
        """
        f_calc_treatment = round(self.mid_square_treatment() / self.mid_square_error(), 2)
        if self.block:
            f_calc_block = round(self.mid_square_block() / self.mid_square_error(), 2)
            return (f_calc_treatment, f_calc_block)
        return (f_calc_treatment,)

    def f_95_table(self):
        """
        generate F table with 95% accuracy
        """
        f_95_treatment = round(f.ppf(0.95, self.db_index()[0], self.db_index()[2]), 2)
        if self.block:
            f_95_block = round(f.ppf(0.95, self.db_index()[3], self.db_index()[2]), 2)
            return (f_95_treatment, f_95_block)
        return (f_95_treatment,)

    def f_99_table(self):
        """
        generate F table with 99% accuracy
        """
        f_99_treatment = round(f.ppf(0.99, self.db_index()[0], self.db_index()[2]), 2)
        if self.block:
            f_99_block = round(f.ppf(0.99, self.db_index()[3], self.db_index()[2]), 2)
            return (f_99_treatment, f_99_block)
        return (f_99_treatment,)
        
    def anova_table(self):
        """
        generate anova table
        """
        status_treatment = 'ns'
        if self.f_calc()[0] > self.f_99_table()[0]:
            status_treatment = 'vs'
        elif self.f_calc()[0] > self.f_95_table()[0]:
            status_treatment = 's'

        if self.block:
            status_block = 'ns'
            if self.f_calc()[1] > self.f_99_table()[1]:
                status_block = 'vs'
            elif self.f_calc()[1] > self.f_95_table()[1]:
                status_block = 's'

            print("SK\tDB\tJK\tKT\tF Hitung\t F tabel")
            print('\t\t\t\t\t\t5%\t1%')
            print('K\t{0}\t{1}\t{2}\t{3}{4}\t\t{5}\t{6}'.format(self.db_index()[3], self.sum_square_block(), self.mid_square_block(), self.f_calc()[1], status_block, self.f_95_table()[1], self.f_99_table()[1]))
            print('T\t{0}\t{1}\t{2}\t{3}{4}\t\t{5}\t{6}'.format(self.db_index()[0], self.sum_square_treatment(), self.mid_square_treatment(), self.f_calc()[0], status_treatment, self.f_95_table()[0], self.f_99_table()[0]))
            print('Galat\t{0}\t{1}\t{2}'.format(self.db_index()[2], self.sum_square_error(), self.mid_square_error()))
            print('Total\t{0}\t{1}'.format(self.db_index()[1], self.sum_square_total()))

        else:

            print("SK\tDB\tJK\tKT\tF Hitung\t F tabel")
            print('\t\t\t\t\t\t5%\t1%')
            print('T\t{0}\t{1}\t{2}\t{3}{4}\t\t{5}\t{6}'.format(self.db_index()[0], self.sum_square_treatment(), self.mid_square_treatment(), self.f_calc()[0], status_treatment, self.f_95_table()[0], self.f_99_table()[0]))
            print('Galat\t{0}\t{1}\t{2}'.format(self.db_index()[2], self.sum_square_error(), self.mid_square_error()))
            print('Total\t{0}\t{1}'.format(self.db_index()[1], self.sum_square_total()))



"""
Function method -- earlier experiment
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

    mid_square_treatment = round(treatment_sum_square / db_treatment, 2) # KTP
    mid_square_error = round(error_sum_square / db_error, 2) # KTG

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
])"""