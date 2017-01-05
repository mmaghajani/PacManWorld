fruitPrices = {'apples': 2.00, 'oranges': 1.50, 'pears': 1.75}


def buy_fruit(fruit, num_pounds):
    if fruit not in fruitPrices:
        print "Sorry we don't have %s" % fruit
    else:
        cost = fruitPrices[fruit] * num_pounds
        print "That'll be %f please" % cost


# Main Function
if __name__ == '__main__':
    buy_fruit('apples', 2.4)
    buy_fruit('coconuts', 2)
