from datetime import timedelta, datetime
from random import choice, randint, randrange, getrandbits
from string import ascii_letters as letters

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from pandas.util.testing import randbool

from sc.models import Comment, CreativeType
from sc.models import Submission
from users.models import ScUser


class Command(BaseCommand):
    help = 'Generates tests data'

    def add_arguments(self, parser):
        parser.add_argument('--thread_count', type=int, default=10)
        parser.add_argument('--root_comments', type=int, default=10)

    def getRandomCT(self):
        id_list = CreativeType.objects.all().values_list('id', flat=True)
        # print(id_list)
        rid = choice(id_list)
        return CreativeType.objects.get(pk=rid)

    def handle(self, *args, **options):
        CreativeType.objects.get_or_create(name='Видео'),
        CreativeType.objects.get_or_create(name='Дизайн'),
        CreativeType.objects.get_or_create(name='Концепция'),
        CreativeType.objects.get_or_create(name='Сюжет'),
        CreativeType.objects.get_or_create(name='Музыка'),
        CreativeType.objects.get_or_create(name='Изобретения'),

        admin = self.get_or_create_author('admin', '027ae9e272ad001b3542b880d47d67b9')
        admin.user.is_staff = True
        admin.user.is_superuser = True
        admin.user.save()
        self.get_or_create_author('moderator', 'c4989a3ad5c100c33a4fdaf0493f4c2b')
        self.get_or_create_author('aoklyunin', 'aoklyunin1990')

        self.links = [
            '', '', '', '', '', '', '',
            'https://www.youtube.com/watch?v=qbfv7fehp0c',
            'https://www.youtube.com/watch?v=w5643H7YsDs',
            'https://www.youtube.com/watch?v=JNzRtoPVALs',
            'https://www.youtube.com/watch?v=3ocqMsoY8oI',
            'https://www.youtube.com/watch?v=Wljrq_Uv_DY',
            'https://www.youtube.com/watch?v=q7AoF7WNjGU',
            'https://www.youtube.com/watch?v=DpBlTyQSAMc',
            'https://www.youtube.com/watch?v=LgTgp0btph8',
            'https://stackoverflow.com/questions/48074967/image-doesnt-stay-in-the-center-when-resizing-windows',
            'https://stackoverflow.com/questions/48074964/get-coordinates-of-an-image-java',
            'https://stackoverflow.com/questions/48074877/firebase-crashlytics-not-showing-crash-report-in-console-dashboard-swift',
            'https://stackoverflow.com/questions/48074950/how-to-get-package-name-of-any-app-when-it-gets-opened-by-user',
            'https://stackoverflow.com/questions/48074939/upgrade-from-qt-5-7-to-5-10-results-in-slower-ui',
            'https://stackoverflow.com/questions/42372698/sonarqube-cake-and-teamcity-integration-issue',
            '<a data-flickr-embed="true"  href="https://www.flickr.com/photos/lindypfaff/11891185725/in/feed" title="11 | 365 - negative space"><img src="https://farm4.staticflickr.com/3701/11891185725_d481460051_o.jpg" width="900" height="599" alt="11 | 365 - negative space"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>',
            '<a data-flickr-embed="true"  href="https://www.flickr.com/photos/zeeyolqpictures/8304251137/in/feed" title="baby"><img src="https://farm9.staticflickr.com/8082/8304251137_5af27cabb8_b.jpg" width="1024" height="576" alt="baby"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>',
            '<a data-flickr-embed="true"  href="https://www.flickr.com/photos/romyspic/15882039437/in/feed" title="Christmas at Nubble"><img src="https://farm8.staticflickr.com/7528/15882039437_fa96c20d07_b.jpg" width="1024" height="683" alt="Christmas at Nubble"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>',
            '<a data-flickr-embed="true"  href="https://www.flickr.com/photos/garethbragdon/12468513504/in/feed" title="Untitled"><img src="https://farm4.staticflickr.com/3731/12468513504_401b9bf4a8_b.jpg" width="1024" height="683" alt="Untitled"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>',
            '<a data-flickr-embed="true"  href="https://www.flickr.com/photos/inestakesphotos/6985559497/in/feed" title="Tiny Home"><img src="https://farm8.staticflickr.com/7199/6985559497_185f8bdcab_b.jpg" width="1024" height="713" alt="Tiny Home"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>',
            '<a data-flickr-embed="true"  href="https://www.flickr.com/photos/albertdros/17320009452/in/feed" title="Dutch Milkyway"><img src="https://farm8.staticflickr.com/7670/17320009452_91e18c9a59_b.jpg" width="1024" height="451" alt="Dutch Milkyway"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>',
            '<a data-flickr-embed="true"  href="https://www.flickr.com/photos/arken-zi-lar/14508615245/in/feed" title="Simple solution"><img src="https://farm3.staticflickr.com/2930/14508615245_f153a9d375_b.jpg" width="1024" height="683" alt="Simple solution"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>',
            '<a data-flickr-embed="true"  href="https://www.flickr.com/photos/jacoboson/16526732367/in/feed" title="a clockwork orange"><img src="https://farm9.staticflickr.com/8650/16526732367_88eb2b7ec6_b.jpg" width="1024" height="683" alt="a clockwork orange"></a><script async src="//embedr.flickr.com/assets/client-code.js" charset="utf-8"></script>',
            '<iframe width="100%" height="300" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/314854552&amp;color=%23ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false&amp;show_teaser=true&amp;visual=true"></iframe>',
            '<iframe width="100%" height="300" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/312423882&amp;color=%23ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false&amp;show_teaser=true&amp;visual=true"></iframe>',
            '<iframe width="100%" height="300" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/14702278&amp;color=%23ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false&amp;show_teaser=true&amp;visual=true"></iframe>',
            '<iframe width="100%" height="300" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/55979319&amp;color=%23ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false&amp;show_teaser=true&amp;visual=true"></iframe>',
            '<iframe width="100%" height="300" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/55972876&amp;color=%23ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false&amp;show_teaser=true&amp;visual=true"></iframe>',
            '<iframe width="100%" height="300" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/50349529&amp;color=%23ff5500&amp;auto_play=false&amp;hide_related=false&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false&amp;show_teaser=true&amp;visual=true"></iframe>',
        ]

        self.captions = [
            'Заголовок 1',
            'Продавец тот ещё тролль)',
            'Первое фото в 2018 и такое удачное',
            'Рассвет в кабине',
            'Блеснула полушариями',
            'Все эти шоу про новоселье такие одинаковые',
            'Еще позитив про корпоратив. Хоть его и не было',
            'Автомобили #26. Ford 021C',
            'Куда обращаться?',
            'Любовь к человечеству.',
            'Когда неважно, сколько денег ушло...',
            'Поехали за грибами, а нашли следы применения неведомого по мощности оружия.',
            'Адекватность',
            'Онлайн музеи и онлайн архивы.',
            'Действенный метод против всяких негодяев',
            'Мне нравится эта новость!!!',
            'Зима 2018)',
            'Спасибо за сердечный приступ, Реймонд',
            'О честности "Столото"',
            'Вот когда руки откуда нужно растут.',
            'Что это за штука? - 17',
            'Про Роснефть и их отношение к детям и спорту',
        ]

        self.textes = [
            '', '', '', '', '', '', '', '', '', '', '',
            "Мне 27 лет и я тренер по плаванию в небольшом городе восточной сибири, в котором градообразующим предприятием является компания Роснефть. У нас НПЗ, завод масел, вобщем у нас делают всё: бензин, масла и прочее. Практически в каждой семье нашего города есть человек работающий в Роснефти и средняя зарплата там 30-35 тысяч рублей.. Это я написал, чтоб был понятен масштаб влияния этой компании на жизнь города.",
            "Теперь вернусь непосредственно к сути.. В городе у нас 6 бассейнов из которых 3 принадлежат вышеупомянутой компании, один муниципальный и два частных. При населении около 300 тысяч человек муниципального и двух частных бассейнов очень не хватает для детей, тем более что в частных бассейнах цена сразу отсеивает определенный контингент родителей, не имеющих возможности отдать ребёнка в секцию плавания за запрашиваемую сумму. Я, как тренер, работал несколько лет в одном из частных бассейнов, но три года назад отделился и организовал маленький плавательный клуб. Плавать мы стали в бассейне на базе отдыха, за чертой города, который принадлежит компании роснефть. Цена на занятия стала дешевле чем в других бассейнах, что безусловно было приятно для родителей. Сразу поясню, что никаким бизнесменом я не являюсь и кучи денег не зарабатываю, напротив, я постоянно балансирую на грани, вкладываю в выдающихся детей средства которые несу с другой работы, благо что жена пока относится с пониманием. Вообще хотел сменить род деятельности, но родители, занимающихся у меня детей, очень просили не бросать их.",
            "ороче сначала мне казалось, что Роснефть - это же огромная, государственная компания, которая яро выступает за спорт и заявляет о необходимости присутсвия спорта в жизни людей, где я обязательно найду поддержку и понимание.. но не тут то было.",
            "Началось все с того, что персонал этого бассейна ополчился на меня и на детей из-за того что им прибавилось работы.. они так и говорили: раньше мы сидели здесь спокойно, в тишине, и получали свой оклад, а теперь нам приходится пол протирать, куртки в гардероб вешать",
            ".. они грубили детям, родителям, прятали и даже выбрасывали наш инвентарь, всячески пытались отбить у нас желание пользоваться их бассейном.",
            "Чтоб было понятно, родители платили в бассейне на общих условиях, никаких скидок мне выпросить не удалось и сумма которая поступала именно от нас составляла больше четверти, а иногда и больше половины дохода бассейна.",
            "Более того, т.к. я являюсь ярым популяризатором спорта в нашем городе и плавания в частности , со мной в этот некогда пустой и никому ненужный бассейн пришло много любителей плавания, что значительно увеличило прибыль этого бассейна. Но как раз это и раздражало тогдашнего руководителя той базы отдыха, потому что ему прибыль погоды не делала, она уходила прямиком в Москву, а бассейн построенный Роснефтью стоял себе нетронутый и блестел, как новый, за что местное вышестоящее руководство его хвалило.",
            "На все мои просьбы и мольбы дать детям спокойно тренироваться никто не реагировал положительно, напротив, они поднимали цены в этом бассейне, в надежде избавиться наконец от нас.",
            "Со временем персонал слегка успокоился и свыкся с мыслью о том, что я настырней их и буду и впредь отстаивать возможность детей плавать там, но вежливостью так и не разжился. А я в свою очередь знал, за что я борюсь и почему терплю такое отношение. ",
            "Но оказалось, что терпеть такое- это не так уж страшно, по сравнению с тем, что началось после..",
            "Один руководитель сменился другим и он оказался моим знакомым, я работал как то летом у него в детском лагере и он прекрасно знал меня, моё отношение к спорту и детям. Он был лоялен ко мне, он был за детей, как и я, и постепенно наши отношения с персоналом того бассейна перестали быть такими напряженными, нас перестали тюкать и пытаться выкурить. Но, как говорится, затишье бывает перед бурей. ",
            "Сначала мне запретили тренировать детей в определённые дни недели и часы, мотивируя это решение тем что дети мешают плавать взрослым, что привело к завершению занятий плаванием для 50 детей. При этом я показывал фотографии пустой чаши бассейна в эти дни, никого кроме детей там никогда и не было, мы пришли в этот бассейн когда он был вообще пустой.",
            "Затем меня запоздало уведомили, о том что в очередной раз поднялась цена в бассейне, именно для детей, что стало для существования нашей маленькой команды пловцов серьёзной проблемой, но мы нашли выход, договорившись с лояльным директором бассейна.",
            "Но затем, в конце декабря, уже прошлого года, тому самому лояльному к детям руководителю позвонил начальник отдела маркетинга и развития бизнеса управления социальной культуры и спорта",
            " Роснефти нашего города и сказал ему, что если он будет идти на уступки пловцам, то его уволят, чтоб с нас брали деньги по полной программе по новым расценкам, что на данный момент является для 80% родителей непосильной суммой и означает конец существования плавательного клуба и завершение тренировок для детей.",
            "Я не знаю как оправдать и объяснить действия этих роснефтефских начальников, не знаю кого ещё попросить о помощи и кому рассказать об этом отношении.. для меня и родителей моих спортсменов, выступающих на соревнованиях разного уровня, эти обстоятельства кажутся абсурдными и мы не можем понять на сколько нужно ненавидеть детей, чтоб так противостоять детскому спорту."
        ]

        self.thread_count = 20
        self.root_comments = 5

        self.random_usernames = ['PIBtKi', 'qKhGhI', 'zQSKWS', 'TfwsZy', 'EjBUtD', 'jRxPPe', 'PXhXnn', 'KCFXng',
                                 'CbZJwD', 'UXZODC', 'cVyzxd', 'fGzlKD', 'ecyrsT', 'XGbBFR', 'UcPZpw', 'CvuHwp',
                                 'zoUyAV', 'ALabKK', 'NGYkJo', 'skhUIC']

        for index in range(self.thread_count):
            print("Thread {} out of {}".format(str(index), self.thread_count))
            selftext = self.get_random_sentence()
            title = choice(self.captions)
            author = self.get_or_create_author(choice(self.random_usernames))
            ups = randint(0, 1000)
            url = choice(self.links)
            downs = int(ups) / 2
            comments = 0

            category = randint(0, 1)
            submission = Submission(author=author,
                                    title=title,
                                    url=url,
                                    text=selftext,
                                    ups=int(ups),
                                    viewCnt=randint(0, 100),
                                    downs=downs,
                                    score=ups - downs,
                                    comment_count=comments,
                                    tp=category
                                    )
            submission.processUrl()
            if category == Submission.TP_CHALLENGE:
                if bool(getrandbits(1)):
                    submission.regard = randint(1, 100)
                else:
                    submission.regard = 0
                submission.stoDate = self.random_date()

            submission.generate_html()
            submission.save()
            submission.creativeType.add(self.getRandomCT())
            submission.save()

            for i in range(self.root_comments):
                print("Adding thread comments...")
                comment_author = self.get_or_create_author(choice(self.random_usernames))
                raw_text = self.get_random_sentence(max_words=100)
                new_comment = Comment.create(comment_author, raw_text, submission)
                new_comment.save()
                another_child = choice([True, False])
                while another_child:
                    self.add_replies(new_comment)
                    another_child = choice([True, False])

    def random_date(self):
        """
        This function will return a random datetime between two datetime
        objects.
        """
        days = 60
        int_delta = (days * 24 * 60 * 60)
        random_second = randrange(int_delta)
        return datetime.now() + timedelta(seconds=random_second)

    def get_random_username(self, length=6):
        return ''.join(choice(letters) for _ in range(length))

    def get_random_sentence(self, min_words=6, max_words=100,
                            min_word_len=3,
                            max_word_len=15):
        sentence = ''

        for _ in range(0, randint(min_words, max_words)):
            sentence += ''.join(choice(letters)
                                for i in
                                range(randint(min_word_len, max_word_len)))
            sentence += ' '

        return sentence

    def get_or_create_author(self, username, password=''):
        try:
            user = User.objects.get(username=username)
            author = ScUser.objects.get(user=user)
        except (User.DoesNotExist, ScUser.DoesNotExist):
            print("Creating user {}".format(username))
            new_author = User(username=username)
            if password != '':
                new_author.set_password(password)
            else:
                new_author.set_password(username)
            new_author.save()
            author = ScUser(user=new_author)
            author.save()
        return author

    def add_replies(self, root_comment, depth=1):
        if depth > 5:
            return

        comment_author = self.get_or_create_author(choice(self.random_usernames))

        raw_text = self.get_random_sentence()
        new_comment = Comment.create(comment_author, raw_text, root_comment)
        new_comment.save()
        if choice([True, False]):
            self.add_replies(new_comment, depth + 1)
