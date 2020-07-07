from coffeehouse_nlp.multi_rake import Rake

text_en = (
    '''CoffeeHouse Load Issues

We are experiencing load issues with CoffeeHouse, we are investigating this issue.

This issue will affect LydiaChatBot and CoffeeHouse's API.'''
)

rake = Rake()

keywords = rake.apply(text_en)

print(keywords[:10])
