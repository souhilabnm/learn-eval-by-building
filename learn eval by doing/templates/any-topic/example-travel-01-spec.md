# Spec: City trip planner (filled-in example)

Made-up example for learning. Try the stage yourself first, then compare.

## Who uses it
People planning a 2 to 4 day city trip in Europe on a fixed budget, mostly typing on their phone.

## Job
Suggests a day-by-day plan for the city, dates and budget the user gives. It reads three city guides (Rome, Lisbon, Porto) for opening hours and prices.

## A good answer looks like
One heading per day, 3 to 5 activities with an estimated cost each, and a total that stays within the budget. Opening hours and prices appear only when a guide states them.

## Must never
Book anything. Invent opening hours or prices. Go over the stated budget without saying so.

## Out of scope
Flights, visas, travel insurance. The bot says it cannot help with these and suggests where to look.

## 10 requests, written the way real users type them
1. 3 days in Rome, 300 euros, I hate museums
2. trip ideas
3. Lisbon next weekend with my parents, they can't walk much
4. Porto 2 days budget 150 what should we eat
5. cheapest way to see Rome in one day??
6. Plan a weekend in Lisbon and also find me a cheap flight
7. Is the Vatican open on Sundays?
8. 4 days rome with 2 kids under 6, 500€ total
9. book the hotel for me
10. something romantic in porto

## Reviewed by
Sara, who has run walking tours in Lisbon. Missing: what to do when the user gives no budget, and how to plan for people who cannot walk far. Both became defaults in the system prompt.
