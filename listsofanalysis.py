from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#-----user local permission
from database_setup import Category, Base, ListItem, User
#-----user local permission

from database_setup import Category, Base, ListItem
#engine = create_engine('sqlite:///analysislists.db')

#-----user local permission
engine = create_engine('sqlite:///analysislists_withusers.db')
#-----user local permission

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#-----user local permission
# Create dummy user
User1 = User(name="xinyi wang", email="wxyakx@gmail.com",
            picture='https://lh5.googleusercontent.com/-oVjLgMXoP8I/AAAAAAAAAAI/AAAAAAAAABM/ttxP5BkEoiY/photo.jpg')
session.add(User1)
#session.commit()


# Create dummy user
#User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
#             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
#session.add(User1)
#session.commit()
#-----user local permission

#now added Analysis categories:

#1. Menu for AlphaDiversity
category1 = Category(user_id=1, name = "Alpha diversity")
#category1 = Category(name = "Alpha diversity")

session.add(category1)
session.commit()


listItem1 = ListItem(user_id=1, name = "ace richness index", description = "Here we calculate richness index of ace", category = category1)
#listItem1 = ListItem(name = "ace richness index", description = "Here we calculate richness index of ace", category = category1)

session.add(listItem1)
session.commit()

listItem2 = ListItem(user_id=1, name = "chao richness index", description = "Here we calculate richness index of chao", category = category1)
#listItem2 = ListItem(name = "chao richness index", description = "Here we calculate richness index of chao", category = category1)

session.add(listItem2)
session.commit()

listItem3 = ListItem(user_id=1, name = "shannon diversity index", description = "Here we calculate diversity index of shannon", category = category1)
#listItem3 = ListItem(name = "shannon diversity index", description = "Here we calculate diversity index of shannon", category = category1)

session.add(listItem3)
session.commit()

listItem4 = ListItem(user_id=1, name = "inversesimpson diversity index", description = "Here we calculate diversity index of inversesimpson", category = category1)
#listItem4 = ListItem(name = "inversesimpson diversity index", description = "Here we calculate diversity index of inversesimpson", category = category1)

session.add(listItem4)
session.commit()

#2. Menu for BetaDiversity
category2 = Category(user_id=1, name = "Beta diversity")
#category2 = Category(name = "Beta diversity")

session.add(category2)
session.commit()


listItem1 = ListItem(user_id=1, name = "PCA analysis", description = "Pricinciple Component Analysis is calculated here", category = category2)
#listItem1 = ListItem(name = "PCA analysis", description = "Pricinciple Component Analysis is calculated here", category = category2)

session.add(listItem1)
session.commit()

listItem2 = ListItem(user_id=1, name = "PCoA analysis", description = "Pricinciple Co-ordinates Analysis is calculated here", category = category2)
#listItem2 = ListItem(name = "PCoA analysis", description = "Pricinciple Co-ordinates Analysis is calculated here", category = category2)

session.add(listItem2)
session.commit()

listItem3 = ListItem(user_id=1, name = "PLS-DA analysis", description = "Partial Linear Sequential-DataAnalysis is calculated here", category = category2)
#listItem3 = ListItem(name = "PLS-DA analysis", description = "Partial Linear Sequential-DataAnalysis is calculated here", category = category2)

session.add(listItem3)
session.commit()

#3. Menu for DifferentialAnalysis
category3 = Category(user_id=1, name = "Differential analysis")
#category3 = Category(name = "Differential analysis")

session.add(category3)
session.commit()


listItem1 = ListItem(user_id=1, name = "Heatmap", description = "Various heatmap displays here", category = category3)
#listItem1 = ListItem(name = "Heatmap", description = "Various heatmap displays here", category = category3)

session.add(listItem1)
session.commit()

listItem2 = ListItem(user_id=1, name = "Barplot", description = "Barplot showing taxa differences is displayed here", category = category3)
#listItem2 = ListItem(name = "Barplot", description = "Barplot showing taxa differences is displayed here", category = category3)

session.add(listItem2)
session.commit()

listItem3 = ListItem(user_id=1, name = "Venngraph", description = "Venn graph showing common shared taxa numbers is displayed", category = category3)
#listItem3 = ListItem(name = "Venngraph", description = "Venn graph showing common shared taxa numbers is displayed", category = category3)

session.add(listItem3)
session.commit()

listItem4 = ListItem(user_id=1, name = "streamgraph", description = "Stream line graph showing variations of taxa to time line is displayed", category = category3)
#listItem4 = ListItem(name = "streamgraph", description = "Stream line graph showing variations of taxa to time line is displayed", category = category3)

session.add(listItem4)
session.commit()

listItem5 = ListItem(user_id=1, name = "trendanalysis", description = "Here shows the trend for different substances", category = category3)
#listItem5 = ListItem(name = "trendanalysis", description = "Here shows the trend for different substances", category = category3)

session.add(listItem5)
session.commit()

#after adding pre-defined items, print the results out
print "All predefined analysis items now added (with user)!"
#print "All predefined analysis items now added!"


