class Expense_Splitter():

    """
    Given a CSV file of all expenses output from CommBank.

    Cleans up and returns monthly CSV files to be easily imported into
    personal budget google sheet.
    """


    def __init__(self):
        self.expense_filepath = 'CSVData.csv'
        self.monthly_splits_filepath = 'monthly_splits/'

        self.taxable_categories = [
            'Business expenses',
            'Gaming',
            'Auto & Transport',
            'Bills & utilities',
            'Travel',
            'Financial'
        ]

        self.months = {
            '01': 'January',
            '02': 'February',
            '03': 'March',
            '04': 'April',
            '05': 'May',
            '06': 'June',
            '07': 'July',
            '08': 'August',
            '09': 'September',
            '10': 'October',
            '11': 'November',
            '12': 'December',
        }

        self.expenses_by_month = {
            'July': [],
            'August': [],
            'September': [],
            'October': [],
            'November': [],
            'December': [],
            'January': [],
            'February': [],
            'March': [],
            'April': [],
            'May': [],
            'June': [],
        }


    def run(self):
        expenses = self.read_expenses_from_file()
        expenses = self.convert_expense_strings_to_lists(expenses)
        expenses = self.clean_expense_lists(expenses)

        self.split_total_expenses_monthly(expenses)
        self.output_expenses_to_monthly_csv()


    def read_expenses_from_file(self):
        """ Reads CSV expense list, returns a list of expense strings. """

        with open(self.expense_filepath, 'r') as f:
            return [line.strip() for line in f]


    def convert_expense_strings_to_lists(self, list_of_expense_strings):
        """
        Converts list of expense strings into list of expense lists

        Split into 5 entries:
            - transaction_date
            - value
            - description
            - account_total
            - category
        """

        expense_lists = []
        for expense in list_of_expense_strings:
            expense = expense.strip()
            expense = expense.replace('"', '')
            transaction_date, value, description, account_total, category = expense.split(',')

            expense_lists.append([transaction_date, value, description, account_total, category])

        return expense_lists


    def clean_expense_lists(self, expenses):
        """
         Cleans up the default expense lists.

         Also adds 2 more entries, Taxable and Purchase Date as is relevant
         for each individual expense

         Taxable is determined by a pre-set list of categories.
         Purchase date is the date the transaction was actually purchased, not
         cleared.
         """

        cleaned_expense_list = []

        for (trans_date, value, desc, acc_total, category) in expenses:

            # Purchase date initialisation
            purchase_date = ' ' * 10
            if 'Value Date: ' in desc:
                desc, purchase_date = desc.split('Value Date: ')

            # Taxable initialisation
            if category in self.taxable_categories:
                taxable = 'x'
            else:
                taxable = ''

            # Value cleanup
            if value[0] == '+':
                value = value[1:]

            # Account total cleanup
            if acc_total[0] == '+':
                acc_total = acc_total[1:]

            # Description cleanup
            if 'Transfer to' in desc and category == 'Refund':
                category = ' Transfer'
            elif 'Transfer from' in desc and category == 'Transfer':
                category = 'Refund'

            cleaned_expense_list.append(
                [trans_date, purchase_date, value, acc_total, desc, category, taxable]
            )

        return cleaned_expense_list


    def split_total_expenses_monthly(self, expenses):
        """ Splits the full list of expenses into monthly dicts. """

        for expense in expenses:
            trans_date, *_ = expense
            trans_month = trans_date[3:5]

            self.expenses_by_month[self.months[trans_month]].append(expense)


    def output_expenses_to_monthly_csv(self):
        """ Writes monthly expense lists to individual csv files """

        for month, expenses in self.expenses_by_month.items():

            if not expenses:
                continue

            year = expenses[0][0][8:10]

            with open(f'{self.monthly_splits_filepath}{month} {year}.csv', 'w') as f:
                for expense in reversed(expenses):
                    print(expense)
                    csv_string = ','.join(expense)
                    f.write(f'{csv_string}\n')



splitter = Expense_Splitter()
splitter.run()