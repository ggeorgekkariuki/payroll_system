class KRACalculator:
    name = ''
    basic_salary = 0
    benefits = 0
    overtime = 0
    gross_salary = 0
    NSSF = 0
    taxable_income = 0
    PAYE = 0 #Tax payable
    personal_relief = 2400.00
    after_relief = 0
    chargeable_income = 0 # Before NHIF deduction
    NHIF = 0
    net_salary = 0

    def __init__(self,name,bs,benefits,overtime):
        KRACalculator.name = name
        KRACalculator.basic_salary = bs
        KRACalculator.benefits = benefits
        KRACalculator.overtime = overtime
        KRACalculator.gross_salary_calc(self)
        KRACalculator.nssf_deductions(self)
        KRACalculator.taxable_income_calc(self)
        KRACalculator.monthly_tax_payable(self)
        KRACalculator.personal_relief_deductions(self)
        KRACalculator.chargeable_income_calc(self)
        KRACalculator.nhif_deductions(self)
        KRACalculator.net_salary_calc(self)

    def gross_salary_calc(self):
        self.gross_salary = self.basic_salary + self.benefits + self.overtime

    def nssf_deductions(self):
        if self.gross_salary > 0:
            if self.gross_salary <= 6000: # Tier 1
                self.NSSF = 6 / 100 * self.gross_salary
            elif self.gross_salary <= 18000: # Tier 2
                self.NSSF = (6 / 100 * 6000) + (6 / 100 * (self.gross_salary - 6000))
            elif self.gross_salary > 18000:
                self.NSSF = 6 / 100 * 18000

    def taxable_income_calc(self):
        self.taxable_income = self.gross_salary - self.NSSF

    def monthly_tax_payable(self):
        if self.gross_salary > 0:
            if self.taxable_income < 24001:
                self.PAYE = 10 / 100 * self.taxable_income
            elif self.taxable_income < 32334:
                self.PAYE = (10 / 100 * 24000) + (25 / 100 * (self.taxable_income - 23999))
            elif self.taxable_income > 32333:
                self.PAYE = (10 / 100 * 24000) + (25 / 100 * 8333) + (30 / 100 *(self.taxable_income - 32333))

    def personal_relief_deductions(self):
        if self.gross_salary > 0:
            if self.PAYE > self.personal_relief:
                self.after_relief = self.PAYE - self.personal_relief

        else:
            self.personal_relief = 0

    def chargeable_income_calc(self):
        self.chargeable_income = self.taxable_income - self.after_relief

    def nhif_deductions(self):
        if self.gross_salary > 0 and self.basic_salary >= 1700: # Exclude salaries below the minimum wage
            if self.gross_salary < 6000:
                self.NHIF = 150
            elif self.gross_salary < 8000:
                self.NHIF = 300
            elif self.gross_salary < 12000:
                self.NHIF = 400
            elif self.gross_salary < 15000:
                self.NHIF = 500
            elif self.gross_salary < 20000:
                self.NHIF = 600
            elif self.gross_salary < 25000:
                self.NHIF = 750
            elif self.gross_salary < 30000:
                self.NHIF = 850
            elif self.gross_salary < 35000:
                self.NHIF = 900
            elif self.gross_salary < 40000:
                self.NHIF = 950
            elif self.gross_salary < 45000:
                self.NHIF = 1000
            elif self.gross_salary < 50000:
                self.NHIF = 1100
            elif self.gross_salary < 60000:
                self.NHIF = 1200
            elif self.gross_salary < 70000:
                self.NHIF = 1300
            elif self.gross_salary < 80000:
                self.NHIF = 1400
            elif self.gross_salary < 90000:
                self.NHIF = 1500
            elif self.gross_salary < 100000:
                self.NHIF = 1600
            elif self.gross_salary >= 100000:
                self.NHIF = 1700

    def net_salary_calc(self):
        self.net_salary = self.chargeable_income - self.NHIF
