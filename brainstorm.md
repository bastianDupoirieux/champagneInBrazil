# Main goal of the project

We want to build an application that collectors of items (wine, coffee, spirits, cheese, watches, clothes) that can be kept for a longer time can use to keep an eye on their collection. Our main focus is food related items, but the application can be used for other items such as watches and clothes aswell, although this is not the scope of the project.
We want to offer collectors a convenient way to keep track of the products they own or tried, a geographic visualisation and potentially a recommendation system.

This app should ideally be available on desktop and on different mobile phone systems for a convenient use.


# Idea 1 
A map to locate the exact place where the wine/beans are from
Interactive, with the information on it when you click on the product you own.

# Idea 2 (Priority 1)
A page where you can enter the information on the product you bought
- Name
- Producer
- Domaine
- Product category
- Location (ideally, you enter it and then select a set location offered by the system). Maybe we can get a list of producers even to have the best possible precision, if not then the city.
- Date bought
- Date roasted for beans/vintage for wine
- expiration date (ideally, the system would calculate it by itself)
- option to add one or more pictures of the wine/coffee (including label etc.)
- Space for personal comments and thoughts on the products
- option to say: I own the product/I tried the product (e.g. at a tasting)
- price
- amount of bottles
- where was it bought?
- grape type
- current value/price


In the backend, this information must be sent to a database (question: will it be a local storage system or a global storage system)

Potentially: a recommendation system to fill up some information automatically (important: don't make it too intrusive)

# Idea 3
Dashboard: overview of the cellar/coffee collection:
You can search for something based on keywords (search feature) or you can click and look at the things you own

Have a history of products: products you currently own, products you owned in the past. 
If there is a product you particularly like, you can "add it to favourites" something like that

# Idea 4
The system would highlight the products that need to be consumed fairly soon
Green/yellow/red scale
- White: the wine is too young to drink
- Green: the wine/coffee is good to drink
- Yellow: the wine can be kept if kept in good storage conditions, but you can start thinking about consuming it
- Red: the wine is already past it's ideal keeping time (no matter the conditions you keep it), you should definitely
drink it ASAP

# Idea 5:
A system to help people discover other products that they wouldn't necessarily know
(e.g. if people like a certain Chardonnay, they can try a white wine from another producer)

This should only be kept as an option for clients and not be included into the application so as to keep the gernreal scope of the application a simple cellar management system

# Idea 6

General recommended information on the product
We can use this page to give best practice advice on storage, offer recipes/ideas on what to do (food/wine pairings etc.)
Basically a kind of blog page (maybe at some point, we can get experts on the topic to add some blog entries)