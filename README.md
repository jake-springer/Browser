# Browser
Basic Python browser application with Rich

## Initialize the browser
```
cols = ["name", "age", "location"]
browser = Browser(cols)
```

## Add items to the browser 
```
for person in people_list:
  browser.add_row(person.name, person.age, person.location)
```

## Enter the browser loop
`browser.run()`

## Access user selection
After the browser exits, access the selection with `browser.selected`. This will be a list from the items added when `.add_row()` was called. 
