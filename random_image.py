import random

header_images = [
  'https://i.imgur.com/Eazve8h.png',
  'https://i.imgur.com/6KB5U0y.png',
  'https://i.imgur.com/SlytyUz.png',
  'https://i.imgur.com/guFnrW5.png',
  'https://i.imgur.com/zwz1wla.png',
  'https://i.imgur.com/rh0SKoJ.png',
  'https://i.imgur.com/FvkUUea.png',
  'https://i.imgur.com/QFfaNxs.png',
  'https://i.imgur.com/rXIBDzI.png',
  'https://i.imgur.com/bwcn9Sq.png',
  'https://i.imgur.com/GpnCCcu.png',
  'https://i.imgur.com/wERzsMH.png'
]

def random_image(list):
  for x in range(10):
    random_num = random.randint(1, 11)
  return list[random_num]