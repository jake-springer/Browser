#-----------------------------------------------------
'''
Browser 
1/21/25

Simple browser class used for displaying & searching
data with Rich. 

'''
#----------------------------------------------------


from rich.console import Console 
from rich.table import Table 
from subprocess import call 

console = Console()

def clear():
    call("clear")
    pass

'''
TODO:
[ ]     show() needs to determine if there are items in the self.buffer_items
        list, and if there are, generate pages based on that. Otherwise, 
        just use all items (as it already does).
'''

class Browser:
    def __init__(
        self, 
        # title: str,
        columns: list,
        max_page_length = 5
    ):
        # self.title                  = title 
        self.columns                = columns
        self.table                  = Table()
        self.max_page_length        = max_page_length
        self.items                  = [] # whole item list 
        self.buffer_items           = [] # item set found by search or filters
        self.pages                  = []
        self.current_page           = 0 
        self.next_char              = 'n'
        self.prev_char              = 'p'
        self.title                  = "[green]> BROWSER <"
        self.notice                 = ""
        self.selected               = None 

    def _create_table(self):
        self.table.add_column("no.")
        for col in self.columns:
            self.table.add_column(col)

    def _sort_pages(self):
        self.pages = []
        # 1. no items to sort 
        if not self.items:
            return 
        # Determine if we're using the entire self.items or if there's 
        # items in the buffer. If there's a buffer, load only that as pages. 
        if self.buffer_items:
            items = self.buffer_items
        else:
            items = self.items
        # 2. not enough items for > 1 page
        if len(items) <= self.max_page_length:
            self.pages = [items]
            return 
        # 3. populate pages 
        new_page = []
        for i in items:
            # page isn't full
            if len(new_page) < self.max_page_length:
                new_page.append(i)
            # page is full 
            elif len(new_page) >= self.max_page_length:
                # add the page to the list
                self.pages.append(new_page)
                # reset the new page  
                new_page = [] 
                # start the new page with the item 
                new_page.append(i) 
        # 4. add any remaining items to the last page
        if new_page:
            self.pages.append(new_page) 
        
    def _go_next(self) -> None:
        # at the end, do nothing 
        if self.current_page >= len(self.pages) - 1:
            return 
        else:
            self.current_page += 1
            return 
    
    def _go_prev(self) -> None:
        # at the start, do nothing 
        if self.current_page == 0:
            return 
        else:
            self.current_page -= 1 
            return 

    def _help_menu(self) -> None:
        clear()
        help_table = Table()
        help_table.add_column("command")
        help_table.add_column("description")
        help_table.add_row(self.next_char, "next page")
        help_table.add_row(self.prev_char, "previous page")
        help_table.add_row("search {term}", "search all columns for term")
        help_table.add_row("quit", "exit the browser")
        console.print("[green]Help Menu", justify="center")
        console.print(help_table, justify="center")
        print()
        console.print("Press enter to continue...", justify="center", end="")
        input()

    def _search_all_fields(self, term) -> None:
        '''Search for a term in every sublist in self.items. 
        
        Resets self.buffer_items, and checks for the given term arg 
        in search sublist in self.items. If the item in the sublist matches, the
        entire sublist is added to self.buffer_items 
        Each "sublist" is an item in the self.items list. 
        Example: self.items = [["sublist1", 1], ["sublist2", 2]]
        '''
        self.buffer_items = []
        for item in self.items:
            for field in item:
                if term.lower() in field.lower():
                    self.buffer_items.append(item)
        if self.buffer_items:
            self.notice = "showing results for [green i]" + term.strip()
            self._sort_pages()

    def add_row(self, *args):
        self.items.append([*args])
        # print(self.items)

    def show(self):
        # create a new table object
        self.table = Table()
        self._create_table()
        try:
            page_content = self.pages[self.current_page]
        except IndexError: # fix index error when swapping to a smaller buffer
            self.current_page = 0
            page_content = self.pages[self.current_page]
            self.notice = ""
        console.print(f"Buffer items: " + str(len(self.buffer_items)))
        # add the page items to the table
        for item in page_content: 
            i = page_content.index(item) + 1
            self.table.add_row(f"{str(i)}.", *item)
        if self.title: console.print("[bold green]" + self.title, justify="center")
        console.print(self.table, justify="center")
        console.print(f"[bold]pg. {str(self.current_page + 1)}/{str(len(self.pages))}", justify="center")
        if self.notice: console.print(self.notice, justify="center")

    def run(self):
        # Initial setup
        self._create_table()
        self._sort_pages()
        self.notice = "[i]use \"help\" for controls"
        select_cmds = ["select", "sel", "s"]
        # Loop
        while True:
            clear()
            if self.selected:
                return 
            self.show()
            cmd = input("[?] ").lower()
            if cmd in ["q", "quit", "exit", "bye"]:
                if self.buffer_items:
                    # reset the buffer, start at the beginning 
                    self.buffer_items = []
                    self.current_page = 0
                    self._sort_pages()
                else:
                    clear()
                    return
            # go next
            elif cmd == self.next_char:
                self._go_next()
                self.notice = ""
            # go back
            elif cmd == self.prev_char:
                self._go_prev()
                self.notice = ""
            # show help
            elif cmd in ["h", "help", '?']:
                self._help_menu()
                self.notice = ""
            try:
                args = cmd.split(" ")
                # search 
                if args[0] == "search":
                    term = " ".join(args[1:])
                    self._search_all_fields(term)
                    self.notice = ""
                if args[0].lower() in select_cmds:
                    try:
                        sel = int(args[1].strip()) - 1
                        if sel >= 0: # prevent looping back
                            self.selected = self.pages[self.current_page][sel]
                    except ValueError:
                        self.notice = "enter the no. of the item you want to select"
                    except IndexError:
                        self.notice = "not a valid item no."
            except IndexError:
                pass 
            



if __name__ == "__main__":
    cols = ["Name", "Age", "Location"]
    x = Browser(cols)
    x.add_row("Jake", "25", "Portland")
    x.add_row("Kevin", "25", "Colorado")
    x.add_row("Trevor", "24", "Canby?")
    x.add_row("Tristan", "25", "Gresham")
    x.add_row("Ricky", "18", "Salem")
    x.add_row("Tommy", "40", "Vancouver")
    x.add_row("Gerald", "65", "Maine")
    x.run()
    print(x.selected)
