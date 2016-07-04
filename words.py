english = [word.strip() for word in open("words/english.txt").readlines()]
german = [word.strip() for word in open("words/german.txt").readlines()]
polish = ['nie', 'to', 'się', 'na', 'co', 'że', 'jest', 'do', 'tak', 'jak', 'mnie', 'ale', 'mi', 'za', 'ja', 'ci', 'tu',
          'go', 'tego', 'tym', 'ty', 'czy', 'tylko', 'po', 'jestem', 'cię', 'ma', 'może', 'już', 'mam', 'jesteś', 'pan',
          'coś', 'dla', 'wiem', 'dobrze', 'jeśli', 'od', 'teraz', 'proszę', 'tam', 'wszystko', 'masz', 'więc', 'nic',
          'być', 'będzie', 'gdzie', 'są', 'on', 'mogę', 'ten', 'ciebie', 'sobie', 'wiesz', 'ze', 'bardzo', 'jej',
          'kiedy', 'był', 'jeszcze', 'nas', 'chcę', 'mój', 'było', 'no', 'przez', 'by', 'pani', 'ją', 'jego', 'ich',
          'dlaczego', 'chcesz', 'żeby', 'tutaj', 'mamy', 'też', 'bo', 'dobra', 'kto', 'nigdy', 'przepraszam', 'mu',
          'naprawdę', 'możesz', 'chyba', 'porządku', 'dziękuję', 'muszę', 'panie', 'właśnie', 'ona', 'domu', 'zrobić',
          'nawet', 'gdy', 'prawda', 'te', 'nam', 'będę', 'zawsze', 'bez', 'nim', 'je', 'była', 'jesteśmy', 'dzięki',
          'tej', 'moja', 'trochę', 'ktoś', 'musisz', 'cześć', 'hej', 'lat', 'moje', 'pana', 'musimy', 'dalej', 'twój',
          'wszyscy', 'czas', 'chce', 'który', 'więcej', 'tobą', 'boże', 'powiedzieć', 'sam', 'chodzi', 'czego', 'ta',
          'możemy', 'albo', 'mną', 'razem', 'niech', 'dobry', 'raz', 'stało', 'was', 'czym', 'prostu', 'będziesz',
          'chodź', 'czemu', 'przed', 'ludzi', 'daj', 'ludzie', 'dzień', 'przy', 'życie', 'niż', 'robisz', 'myślę',
          'lepiej', 'kim', 'myślisz', 'miał', 'my', 'nikt', 'czasu', 'powiedz', 'rzeczy', 'twoja', 'tych', 'stąd',
          'niego', 'mówi', 'im', 'temu', 'jeden', 'pod', 'musi', 'siebie', 'twoje', 'powiedział', 'oczywiście', 'ok',
          'moim', 'oni', 'dwa', 'które', 'pewnie', 'dziś', 'kurwa', 'wie', 'taki', 'aby', 'skąd', 'cholera', 'dzieje',
          'wygląda', 'wtedy', 'mojego', 'takie', 'ile', 'wszystkie', 'mieć', 'dlatego', 'znaczy', 'będziemy', 'potem',
          'jasne', 'iść', 'dużo', 'cóż', 'tę', 'byłem', 'rozumiem', 'wam', 'miejsce', 'cały', 'trzeba', 'moją', 'można',
          'pomóc', 'jako', 'nich', 'szybko', 'jakiś', 'mojej', 'nią', 'mają', 'wszystkich', 'jakieś', 'wiedzieć',
          'swoje', 'przykro', 'stary', 'zaraz', 'myśli', 'dzieci', 'nad', 'wiele', 'kochanie', 'kilka', 'mówię',
          'mówisz', 'zanim', 'miałem', 'kocham', 'świetnie', 'tobie', 'takiego', 'tyle', 'robić', 'trzy', 'idź',
          'kogoś', 'ani', 'pewno', 'myślałem', 'widzisz', 'kiedyś', 'robi', 'widzę', 'jaki', 'niej', 'ojciec', 'zbyt',
          'która', 'zobaczyć', 'przestań', 'sposób', 'pracy', 'dzisiaj', 'sie', 'później', 'bardziej', 'będą', 'aż',
          'życia', 'jutro', 'tą', 'rację', 'żebyś', 'długo', 'tato', 'każdy', 'twoim', 'chciałem', 'dni', 'twojej',
          'nadzieję', 'stanie', 'koniec', 'znam', 'mamo', 'swoją', 'problem', 'żyje', 'potrzebuję', 'widziałem',
          'spokój', 'powiem', 'minut', 'broń', 'panu', 'mógł', 'nami', 'wy', 'nocy', 'wciąż', 'znowu', 'pieniądze',
          'imię', 'dnia', 'zabić', 'drzwi', 'pierwszy', 'taka', 'nasz', 'posłuchaj', 'ponieważ', 'słuchaj',
          'jakie', 'gdyby', 'miło', 'spójrz', 'chciałbym', 'sir', 'razie', 'nasze', 'dokładnie', 'czuję', 'zrobił',
          'dobre', 'samo', 'nadal', 'człowiek', 'twoją', 'znaleźć', 'chwilę', 'chciał', 'kogo', 'zostać', 'czegoś',
          'wszystkim', 'został', 'roku', 'mówić', 'jesteście', 'facet', 'mów', 'powiedziałem', 'były', 'którzy',
          'dziecko', 'idziemy', 'sama', 'macie', 'mówiłem', 'we', 'napisy', 'mogą', 'spokojnie', 'sobą', 'bym', 'miała',
          'przecież', 'dom', 'poza', 'zamknij', 'byłeś', 'lubię', 'oh', 'żadnych', 'pomocy', 'prawie', 'gdzieś',
          'porozmawiać', 'wcześniej', 'podoba', 'zrobię', 'czekaj', 'dość', 'twojego', 'lub', 'moich', 'razy', 'znasz',
          'mały', 'ciągle', 'jakby', 'wydaje', 'mama', 'powinniśmy', 'jeżeli', 'jack', 'powinieneś', 'innego', 'sprawy',
          'rozumiesz', 'trzymaj', 'końcu', 'powodu', 'jedno', 'pamiętasz', 'pomysł', 'noc', 'pewien', 'którą', 'wiemy',
          'bądź', 'żebym', 'numer', 'oczy', 'lata', 'dwie', 'miejscu', 'dokąd', 'och', 'pokoju', 'chodźmy', 'ojca',
          'weź', 'idę', 'samochód', 'nowy', 'jednak', 'świat', 'źle', 'którego', 'niczego', 'oto', 'dwóch', 'sprawa',
          'swój', 'idzie', 'takim', 'jedną', 'wystarczy', 'byłam', 'rano', 'nimi', 'halo', 'byś', 'życiu', 'całe',
          'wiedziałem', 'swojego', 'śmierć', 'ręce', 'musiał', 'którym', 'całą', 'chcą', 'da', 'właściwie', 'zrób',
          'panowie', 'skoro', 'drogi', 'czujesz', 'dam', 'pozwól', 'wyglądasz', 'jednego', 'jedna', 'mówił', 'których',
          'świecie', 'patrz', 'nikogo', 'byli', 'pytanie', 'swoim', 'której', 'powinienem', 'jezu', 'dać', 'rzecz',
          'powiedziała', 'powiedziałeś', 'najpierw', 'sądzę', 'prawo', 'matka', 'widzieć', 'john', 'dr', 'telefon',
          'podczas', 'wczoraj', 'śmierci', 'pracę', 'pamiętam', 'uważaj', 'parę', 'wrócić', 'diabła', 'the', 'robię',
          'zrobiłem', 'kobiety', 'poważnie', 'miejsca', 'znów', 'cholery', 'zrobiłeś', 'sprawę', 'zaczekaj', 'powiesz',
          'rób', 'natychmiast', 'dziewczyna', 'również', 'działa', 'słyszałem', 'pięć', 'super', 'swoich', 'mówią',
          'witam', 'całkiem', 'cokolwiek',
          ]
slovenian = ['je', 'in', 'se', 'v', 'da', 'na', 'so', 'ne', 'pa', 'ki', 'bi', 'za', 'z', 'ni', 'sem', 'ga', 'še', 'po',
             's', 'tako', 'ko', 'tudi', 'to', 'bil', 'ali', 'si', 'mu', 'od', 'bilo', 'kot', 'že', 'iz', 'kaj', 'bo',
             'če', 'vse', 'bila', 'kakor', 'mi', 'pri', 'jo', 'kar', 'jih', 'sta', 'o', 'do', 'ti', 'kako', 'samo',
             'me']
manual = ["run", "oh", "such", "yo", "sure", "i'm", "love", "can't", "yourself", "open", "they're", 'i\'ll',"it's",'never','easy',"sitting","simultaneous","release"]
most_common = set(manual + english + slovenian + polish +german)
