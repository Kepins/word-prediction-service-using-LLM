import concurrent.futures
import random
import http.client
import json
import time
import statistics

# Define the endpoint and predefined list of values
host = "127.0.0.1"
port = 8080
url = "/"
# payload_values = [
#     "Każdego ranka, gdy wstaję z łóżka, otwieram okno, aby zaczerpnąć świeżego powietrza i zobaczyć, jak zaczyna się nowy dzień. Zastanawiam się, co mnie dzisiaj czeka, jakie rozmowy będę prowadzić i z kim się spotkam. W takich chwilach, pełen ciekawości i optymizmu, najchętniej witam bliskich, znajomych lub kolegów z pracy prostym pytaniem, które pozwala mi nawiązać rozmowę. Dzień dobry, jak się",
#     "Po intensywnym poranku pełnym obowiązków, jak sprzątanie kuchni, robienie zakupów i odbieranie dzieci ze szkoły, w końcu mogłem usiąść na chwilę, żeby zastanowić się, co ugotować na obiad. Chciałem, żeby to było coś pysznego, pożywnego i takiego, co sprawi, że cała rodzina będzie zadowolona. Patrząc na półki w kuchni i rozważając różne opcje, wpadłem na pomysł, który wydawał się idealny. Na obiad ugotuję zupę",
#     "Długie godziny spędzone w ogrodzie na grabieniu liści i pielęgnacji kwiatów sprawiły, że poczułem zmęczenie, a do tego zaczęło mi brakować pewnych rzeczy, które są niezbędne do dalszej pracy. Spojrzałem w stronę sąsiada, który zawsze chętnie pomaga, i postanowiłem zapytać, czy mógłby się ze mną podzielić tym, czego akurat potrzebuję. Zastanawiając się, jak najlepiej wyrazić moją prośbę, powiedziałem: Czy mogę prosić o trochę",
#     "W ciepłe sobotnie popołudnie siedzieliśmy z przyjaciółmi w ogrodzie, rozmawiając o tym, jak możemy spędzić resztę dnia, żeby wykorzystać dobrą pogodę. Padły różne pomysły: wypad na rowery, wyjście na lody, a może spacer po parku lub lesie. W końcu zgodziliśmy się, że nic nie przebije wycieczki do miejsca, które wszyscy uwielbiamy. Z entuzjazmem oznajmiłem: Idziemy dzisiaj na spacer do",
#     "Podczas porannego biegu zauważyłem, że świat wokół mnie wygląda zupełnie inaczej niż zazwyczaj. Niebo miało niezwykły kolor, wiatr przyjemnie chłodził twarz, a zapach wilgotnej trawy dodawał energii. Zastanawiając się, jak najlepiej opisać ten wyjątkowy dzień, który zdecydowanie różnił się od pozostałych, pomyślałem o jednym słowie, które idealnie oddaje moje wrażenia. Pogoda jest dzisiaj bardzo",
#     "Wieczorem, kiedy zmęczony pracą usiadłem na kanapie, pomyślałem, że zasługuję na chwilę relaksu. Włączyłem telewizor, przeszukując kanały w poszukiwaniu czegoś, co mogłoby mnie wciągnąć i oderwać od codziennych zmartwień. Po kilku minutach trafiłem na film, który od razu przykuł moją uwagę swoją fabułą, postaciami i pięknymi ujęciami. Bez wahania postanowiłem go obejrzeć, a później opowiedzieć o tym znajomym. Wczoraj wieczorem oglądałem świetny",
#     "Od wielu miesięcy myślałem o tym, jak bardzo potrzebuję odpoczynku od codziennych obowiązków i monotonii. Przeglądając katalogi biur podróży, oglądałem piękne zdjęcia plaż, górskich szlaków i tętniących życiem miast. Każda z tych destynacji wydawała się kusząca, ale w końcu zdecydowałem się na jedno miejsce, o którym marzyłem od dawna. W głowie już widzę, jak spędzam tam dni pełne relaksu i przygód. Chciałbym pojechać na wakacje do",
#     "Gdy usiadłem w ulubionej kawiarni w centrum miasta, kelnerka podeszła do mojego stolika z uśmiechem, pytając, co chciałbym zamówić. Rozejrzałem się po menu, szukając czegoś, co idealnie pasowałoby do tego leniwego popołudnia. Po krótkim zastanowieniu zdecydowałem się na coś klasycznego, ale zawsze pysznego i kojącego. Spojrzałem na nią i powiedziałem: Poproszę o kawę z mlekiem i",
#     "W piątkowy wieczór siedzieliśmy z rodziną w salonie, rozmawiając o tym, jak spędzimy nadchodzącą sobotę. Rozważaliśmy różne opcje: może piknik w parku, wycieczka do muzeum albo wizyta w zoo. W końcu jednogłośnie zgodziliśmy się na coś, co zawsze sprawia nam radość i pozwala aktywnie spędzić czas razem. Z entuzjazmem powiedziałem: W sobotę wybieramy się na",
#     "Po przebudzeniu w sobotni poranek poczułem zapach świeżego pieczywa, które mama przyniosła z piekarni. Wiedziałem, że czeka mnie pyszne śniadanie, które doda mi energii na cały dzień. Otworzyłem lodówkę i zacząłem wybierać składniki, zastanawiając się, na co mam największą ochotę. W końcu zdecydowałem się na klasyczną kombinację, która nigdy mnie nie zawodzi. Na śniadanie zjadłam chleb z",
#     "Gdy wracałem z pracy, zauważyłem na wystawie sklepowej coś, co od razu przyciągnęło moją uwagę. Nie mogłem się powstrzymać i postanowiłem to kupić, bo idealnie pasowało do mojego stylu i potrzeb. Po powrocie do domu z niecierpliwością pokazałem to mojej rodzinie, oczekując ich reakcji. Z uśmiechem zapytałem: Czy widziałeś mój nowy",
#     "Po wielu miesiącach mieszkania w tym samym pokoju poczułem, że nadszedł czas na zmiany. Rozmawiałem z rodziną o możliwościach odświeżenia wnętrza, które sprawiłoby, że nasz dom stanie się bardziej przytulny i estetyczny. Zdecydowaliśmy, że najlepszym pomysłem będzie przemalowanie ścian na kolor, który od dawna nam się podobał. W weekend planujemy malować ściany na",
#     "Każdego ranka, przed wyjściem do szkoły, pakuję plecak, upewniając się, że zabrałem wszystko, co jest mi potrzebne. W środku zawsze znajduje się kilka niezbędnych rzeczy, które pomagają mi przetrwać dzień, od zeszytów i podręczników po przekąski na przerwę. Czasem zastanawiam się, jak wyglądałby mój dzień, gdyby zabrakło jednej z tych rzeczy. Do szkoły zawsze noszę w plecaku",
#     "Podczas wizyty na rynku zobaczyłem stoisko pełne kolorowych i świeżych owoców. Pachniały tak intensywnie, że nie mogłem się oprzeć, by sięgnąć po jeden z nich. Zawsze miałem słabość do tego jednego, wyjątkowego owocu, który przypomina mi dzieciństwo i lato. Nie mogłem się powstrzymać, by o tym opowiedzieć: Mój ulubiony owoc to",
#     "Kiedy sprzątałem pokój, zauważyłem, że brakuje jednej z moich ulubionych rzeczy. Przeszukałem wszystkie szuflady, zaglądałem pod łóżko, ale nigdzie jej nie było. W końcu postanowiłem poprosić o pomoc kogoś z domowników, mając nadzieję, że razem uda nam się to znaleźć. Z lekkim zmartwieniem zapytałem: Czy pomożesz mi znaleźć moje",
#     "Kilka dni temu, późnym wieczorem, postanowiłem poświęcić czas na czytanie książki, którą dostałem od przyjaciela. Już od pierwszych stron wciągnęła mnie historia, a sposób, w jaki była napisana, sprawił, że nie mogłem się od niej oderwać. Gdy skończyłem, miałem ochotę opowiedzieć o niej każdemu, kogo znam. Książka, którą ostatnio czytałem, była bardzo",
#     "Na moich urodzinach zebrało się wielu bliskich mi ludzi, każdy z nich przyniósł ze sobą prezent. Po rozpakowaniu wszystkich paczek natknąłem się na coś, co szczególnie mnie urzekło. Był to piękny przedmiot, który od razu znalazł honorowe miejsce w moim domu. Gdy wspominałem ten dzień, powiedziałem: Na urodziny dostałem piękny",
#     "Pracując nad ważnym projektem, zdałem sobie sprawę, że nie mogę polegać tylko na swojej pamięci. Wszystkie ważne szczegóły musiałem gdzieś zanotować, aby niczego nie przeoczyć. Wziąłem kawałek papieru i zacząłem spisywać wszystko, co przyszło mi do głowy, mówiąc: Proszę zapisać to na kartce",
#     "Gdy sprawdzaliśmy repertuar kina, długo debatowaliśmy nad tym, jaki film wybrać. W końcu zdecydowaliśmy się na coś, co wydawało się fascynujące i pełne akcji. Już teraz nie mogę się doczekać, kiedy usiądę w wygodnym fotelu i zanurzę się w tę historię. Wieczorem pójdziemy do kina na",
#     "Od dziecka fascynował mnie pewien kolor, który zawsze wywoływał we mnie spokój i radość. W moich ubraniach, dodatkach czy dekoracjach wnętrz staram się używać właśnie tej barwy, bo sprawia, że czuję się lepiej. Często dzielę się moimi upodobaniami z innymi, mówiąc: Moim ulubionym kolorem jest",
# ]

payload_values = [
    "Kocham czytać ",
    "Lubię biegać po ",
    "Czuję radość, gdy słucham ",
    "Pamiętam wspaniałe chwile z ",
    "Chciałbym odwiedzić ",
    "Widzę piękne krajobrazy w tym ",
    "Jem smaczne jedzenie z ",
    "Lubię rozmawiać o ",
    "Czuję się szczęśliwy, gdy ",
    "Kocham oglądać zachody ",
    "Biegam codziennie ",
    "Pamiętam każdą podróż, którą ",
    "Lubię gotować nowe ",
    "Chciałbym poznać nowe ",
    "Widzę w przyszłości wiele ",
    "Czuję spokój, gdy ",
]


# Function to send a single PUT request
def send_request():
    payload = {"prompt": random.choice(payload_values)}
    headers = {"Content-Type": "application/json"}
    try:
        conn = http.client.HTTPConnection(host, port)
        start_time = time.time()
        conn.request("PUT", url, json.dumps(payload), headers)
        response = conn.getresponse()
        end_time = time.time()
        return response.status, response.read().decode(), (end_time - start_time)
    except Exception as e:
        return None, str(e), None
    finally:
        conn.close()


# Stress test configuration
num_requests = 10240  # Total number of requests
max_workers = 128  # Maximum number of concurrent workers


# Function to run the stress test
def run_stress_test():
    print(f"Starting stress test with {num_requests} requests and {max_workers} workers...")

    results = []
    response_times = []
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(send_request) for _ in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            if result[2] is not None:
                response_times.append(result[2])
    duration = time.time() - start_time

    # Log results
    success_count = sum(1 for result in results if result[0] == 200)
    failure_count = len(results) - success_count

    print(f"\nStress Test Results:")
    print(f"Successful requests: {success_count}")
    print(f"Failed requests: {failure_count}")

    if response_times:
        avg_time = statistics.mean(response_times)
        std_dev_time = statistics.stdev(response_times)
        max_time = max(response_times)
        min_time = min(response_times)

        print(f"\nResponse Time Metrics:")
        print(f"Average time per prompt: {(duration / num_requests) * 100:.4f} milliseconds")
        print(f"Average time: {avg_time:.4f} seconds")
        print(f"Standard deviation: {std_dev_time:.4f} seconds")
        print(f"Max time: {max_time:.4f} seconds")
        print(f"Min time: {min_time:.4f} seconds")

    if failure_count > 0:
        print(f"\nErrors:")
        for status, error, _ in results:
            if status != 200:
                print(error)

if __name__ == "__main__":
    run_stress_test()
