"""
Curated Oxford 3000 senses for polysemous words and special Oxford notations.
Guarantees 100% precision for multiple meanings, parenthesized senses, and key exam words.
"""

CURATED_ENTRIES = {
    "abandon": {
        "definition": "to leave a place, person, or thing permanently, or to stop doing something before it is finished",
        "meaningUz": "tashlab ketmoq; tark etmoq",
        "example": "The sailors were forced to abandon the sinking ship during the storm.",
        "exampleUz": "Dengizchilar bo‘ron paytida cho‘kayotgan kemani tark etishga majbur bo‘lishdi."
    },
    "actress": {
        "definition": "a woman who acts in a film, play, or television programme",
        "meaningUz": "aktrisa; kino yoki teatr aktyori (ayol)",
        "example": "The talented actress received an international award for her outstanding performance.",
        "exampleUz": "Iste’dodli aktrisa ajoyib ijrosi uchun xalqaro mukofot oldi."
    },
    "amazing": {
        "definition": "causing great surprise or wonder; extremely good and impressive",
        "meaningUz": "hayratlanarli; ajoyib; lol qoldiradigan",
        "example": "We had an amazing view of the snow-covered mountains from our hotel room.",
        "exampleUz": "Mehmonxona xonamizdan qor bilan qoplangan tog‘larning ajoyib manzarasi ko‘rinib turardi."
    },
    "beautiful": {
        "definition": "very attractive and pleasing to look at, listen to, or experience",
        "meaningUz": "chiroyli; go‘zal",
        "example": "She received a beautiful bouquet of fresh red roses for her birthday.",
        "exampleUz": "U tug‘ilgan kuniga yangi qizil atirgullardan iborat go‘zal guldasta oldi."
    },
    "bank (money)": {
        "definition": "a financial business that keeps money safe, makes loans, and offers financial services",
        "meaningUz": "bank (moliya muassasasi)",
        "example": "I went to the bank this morning to deposit my monthly salary.",
        "exampleUz": "Men bugun ertalab oylik maoshimni qo‘yish uchun bankka bordim.",
        "senses": [
            {
                "definition": "a financial institution that receives deposits and makes loans",
                "meaningUz": "bank",
                "example": "She opened a new savings account at the local bank.",
                "exampleUz": "U mahalliy bankda yangi jamg‘arma hisob raqami ochdi."
            }
        ]
    },
    "bank (river)": {
        "definition": "the sloping ground along the edge of a river, canal, or lake",
        "meaningUz": "daryo qirg‘og‘i",
        "example": "They sat on the grassy bank of the river and enjoyed a quiet picnic.",
        "exampleUz": "Ular daryoning o‘tloqli qirg‘og‘ida o‘tirib, sokin piknikdan zavqlanishdi."
    },
    "light (from the sun/a lamp)": {
        "definition": "the natural or electrical energy that illuminates things and enables sight",
        "meaningUz": "yorug‘lik; chiroq",
        "example": "Please turn on the desk light because it is getting dark in here.",
        "exampleUz": "Iltimos, stol chirog‘ini yoqing, chunki bu yerda qorong‘i tushmoqda.",
        "senses": [
            {
                "definition": "the energy from the sun or a lamp that makes it possible to see",
                "meaningUz": "yorug‘lik",
                "example": "Sunlight streamed in through the open window.",
                "exampleUz": "Ochiq derazadan quyosh nuri tushib turardi."
            },
            {
                "definition": "a lamp or piece of electrical equipment that produces brightness",
                "meaningUz": "chiroq",
                "example": "Remember to switch off all the lights before leaving the house.",
                "exampleUz": "Uydan chiqishdan oldin barcha chiroqlarni o‘chirishni unutmang."
            }
        ]
    },
    "light (not heavy)": {
        "definition": "having little physical weight; not heavy and easy to lift, carry, or move",
        "meaningUz": "yengil; og‘ir bo‘lmagan",
        "example": "Aluminum is a very light metal commonly used in aircraft construction.",
        "exampleUz": "Alyuminiy samolyotsozlikda keng qo‘llaniladigan juda yengil metalldir."
    },
    "like (similar)": {
        "definition": "similar to; having the same characteristics, qualities, or appearance as someone or something",
        "meaningUz": "kabi; o‘xshash",
        "example": "He looks and talks just like his older brother.",
        "exampleUz": "U xuddi akasidek ko‘rinadi va gapiradi."
    },
    "like (find sb/sth pleasant)": {
        "definition": "to enjoy, approve of, or have fond feelings for someone or something",
        "meaningUz": "yoqtirmoq; yaxshi ko‘rmoq",
        "example": "I really like studying foreign languages in my spare time.",
        "exampleUz": "Men bo‘sh vaqtimda chet tillarini o‘rganishni juda yoqtiraman."
    },
    "watch": {
        "definition": "to look at someone or something attentively over a period of time",
        "meaningUz": "tomosha qilmoq; qaramoq (fe’l); qo‘l soati (ot)",
        "example": "We sat down together to watch an interesting documentary on science.",
        "exampleUz": "Biz birgalikda fan haqidagi qiziqarli hujjatli filmni tomosha qilish uchun o‘tirdik.",
        "senses": [
            {
                "definition": "a small clock that is worn on your wrist or carried in a pocket",
                "meaningUz": "qo‘l soati",
                "example": "He checked his watch and realized he was ten minutes late.",
                "exampleUz": "U soatiga qaradi va o‘n daqiqa kechikkanini tushundi."
            },
            {
                "definition": "to look at someone or something carefully for a period of time",
                "meaningUz": "tomosha qilmoq; kuzatmoq",
                "example": "Millions of people watch the Olympic Games on television.",
                "exampleUz": "Millionlab odamlar Olimpiya o‘yinlarini televizor orqali tomosha qilishadi."
            }
        ]
    },
    "play": {
        "definition": "to take part in a game, sport, or fun activity, or perform music",
        "meaningUz": "o‘ynamoq; ijro etmoq (fe’l); pyesa, spektakl (ot)",
        "example": "The children love to play outside in the garden after school.",
        "exampleUz": "Bolalar maktabdan keyin bog‘da ochiq havoda o‘ynashni yaxshi ko‘radilar.",
        "senses": [
            {
                "definition": "to participate in a game or sport for enjoyment or competition",
                "meaningUz": "o‘ynamoq",
                "example": "They play tennis together every Saturday morning.",
                "exampleUz": "Ular har shanba kuni ertalab birga tennis o‘ynashadi."
            },
            {
                "definition": "a dramatic literary work written for actors to perform on a theatre stage",
                "meaningUz": "pyesa; spektakl",
                "example": "Shakespeare wrote many famous historical plays and tragedies.",
                "exampleUz": "Shekspir ko‘plab mashhur tarixiy pyesalar va fojialar yozgan."
            }
        ]
    },
    "break": {
        "definition": "to separate suddenly into pieces as a result of a blow, shock, or strain",
        "meaningUz": "sindirmoq; sinmoq (fe’l); tanaffus (ot)",
        "example": "Be very careful not to drop and break that expensive porcelain vase.",
        "exampleUz": "O‘sha qimmatbaho chinni vazani tushirib yuborib sindirmaslik uchun juda ehtiyot bo‘ling.",
        "senses": [
            {
                "definition": "to cause something to separate into two or more parts abruptly",
                "meaningUz": "sindirmoq; buzmoq",
                "example": "He accidentally broke the ceramic plate while washing dishes.",
                "exampleUz": "U idishlarni yuvayotganda tasodifan sopol likopchani sindirib qo‘ydi."
            },
            {
                "definition": "a pause or short interval of rest from work, study, or physical activity",
                "meaningUz": "tanaffus; dam olish",
                "example": "Let's take a quick fifteen-minute coffee break before continuing.",
                "exampleUz": "Davom ettirishdan oldin o‘n besh daqiqalik qahva tanaffusi qilaylik."
            }
        ]
    },
    "change": {
        "definition": "to make or become different; to transform, exchange, or replace",
        "meaningUz": "o‘zgarmoq; o‘zgartirmoq (fe’l); o‘zgarish; qaytim (ot)",
        "example": "She decided to change her career and become a software developer.",
        "exampleUz": "U kasbini o‘zgartirib, dasturchi bo‘lishga qaror qildi.",
        "senses": [
            {
                "definition": "to make or become different in nature, form, or character",
                "meaningUz": "o‘zgarmoq; o‘zgartirmoq",
                "example": "The leaves on the trees change color during autumn.",
                "exampleUz": "Kuzda daraxtlardagi barglar rangini o‘zgartiradi."
            },
            {
                "definition": "the money returned when the payment given is more than the price charged",
                "meaningUz": "qaytim; mayda pul",
                "example": "Here is your receipt and your change, sir.",
                "exampleUz": "Mana sizning chekingiz va qaytim pulingiz, janob."
            }
        ]
    },
    "run": {
        "definition": "to move fast on foot, or to operate, manage, or maintain something",
        "meaningUz": "yugurmoq; boshqarmoq; ishlamoq",
        "example": "He had to run as fast as possible to catch the morning train.",
        "exampleUz": "U ertalabki poyezdga yetib olish uchun imkon qadar tez yugurishga majbur bo‘ldi.",
        "senses": [
            {
                "definition": "to move along on foot at a pace faster than walking",
                "meaningUz": "yugurmoq",
                "example": "She runs five miles in the park every morning before work.",
                "exampleUz": "U har kuni ertalab ishdan oldin bog‘da besh mil yuguradi."
            },
            {
                "definition": "to direct, control, manage, or operate a business or organization",
                "meaningUz": "boshqarmoq; yurgazmoq",
                "example": "He runs a successful educational center in the city center.",
                "exampleUz": "U shahar markazida muvaffaqiyatli o‘quv markazini boshqaradi."
            }
        ]
    },
    "set": {
        "definition": "to put or place something in a specified position, or a collection of matching things",
        "meaningUz": "o‘rnatmoq; qo‘ymoq (fe’l); to‘plam (ot)",
        "example": "She set the alarm clock for six o'clock in the morning.",
        "exampleUz": "U budilnikni ertalab soat oltiga o‘rnatdi.",
        "senses": [
            {
                "definition": "to adjust, position, or fix something ready for use or operation",
                "meaningUz": "o‘rnatmoq; sozlamoq",
                "example": "He set the thermostat to a comfortable room temperature.",
                "exampleUz": "U termostatni xonaning qulay haroratiga o‘rnatdi."
            },
            {
                "definition": "a collection of matching objects, articles, or books designed for collective use",
                "meaningUz": "to‘plam; to‘da",
                "example": "My grandfather gave me a wooden set of handcrafted chess pieces.",
                "exampleUz": "Bobom menga qo‘lda yasalgan yog‘och shaxmat donalari to‘plamini sovg‘a qildi."
            }
        ]
    },
    "right": {
        "definition": "morally good, factually correct, or the direction opposite to left",
        "meaningUz": "to‘g‘ri; haqiqiy; o‘ng tomon; huquq",
        "example": "Every student in the classroom gave the right answer to the math problem.",
        "exampleUz": "Sinfdagi barcha o‘quvchi matematika masalasiga to‘g‘ri javob berdi.",
        "senses": [
            {
                "definition": "factually correct; accurate, true, and free from error",
                "meaningUz": "to‘g‘ri; xatosiz",
                "example": "Make sure you choose the right option in the multiple-choice test.",
                "exampleUz": "Test savollarida to‘g‘ri variantni tanlaganingizga ishonch hosil qiling."
            },
            {
                "definition": "the side or direction towards the east when facing north; opposite of left",
                "meaningUz": "o‘ng tomon",
                "example": "Turn right at the traffic lights and follow the main street.",
                "exampleUz": "Svetoforda o‘ngga buriling va asosiy ko‘cha bo‘ylab yuring."
            }
        ]
    },
    "mean": {
        "definition": "to express, convey, or intend an idea; or unkind and ungenerous",
        "meaningUz": "anglatmoq; demoqchi bo‘lmoq (fe’l); yovuz, xasis (sifat)",
        "example": "Could you please explain what this complex sentence is supposed to mean?",
        "exampleUz": "Iltimos, bu murakkab gap nima ma’noni anglatishini tushuntirib bera olasizmi?",
        "senses": [
            {
                "definition": "to convey, indicate, or signify a particular thought, concept, or meaning",
                "meaningUz": "anglatmoq; bildirmoq",
                "example": "A red light means that vehicles must come to a complete stop.",
                "exampleUz": "Qizil chiroq transport vositalari to‘liq to‘xtashi kerakligini anglatadi."
            },
            {
                "definition": "unkind, unpleasant, or unwilling to share or spend money",
                "meaningUz": "yovuz; qo‘pol; xasis",
                "example": "It was very mean of him to tease his younger classmate.",
                "exampleUz": "Kichik sinfdoshini masxara qilishi uning juda yomon xulqidan dalolat berardi."
            }
        ]
    },
    "match (contest/correspond)": {
        "definition": "a competitive sports game, or to correspond with or equal something",
        "meaningUz": "o‘yin; musobaqa (ot); mos kelmoq; teng kelmoq (fe’l)",
        "example": "Our school football team won the championship match yesterday.",
        "exampleUz": "Maktabimiz futbol jamoasi kecha chempionat o‘yinida g‘alaba qozondi.",
        "senses": [
            {
                "definition": "a competitive sports contest or game between two people or teams",
                "meaningUz": "musobaqa; o‘yin",
                "example": "We bought front-row tickets for the football match.",
                "exampleUz": "Biz futbol o‘yini uchun old qatordan chiptalar sotib oldik."
            },
            {
                "definition": "to be equal to, correspond with, or complement something harmoniously",
                "meaningUz": "mos kelmoq; mos tushmoq",
                "example": "Her blue scarf matches her beautiful eyes perfectly.",
                "exampleUz": "Uning moviy sharfi chiroyli ko‘zlariga juda mos tushadi."
            }
        ]
    },
    "turn": {
        "definition": "to move in a circular motion, change direction, or a scheduled opportunity",
        "meaningUz": "burilmoq; aylanmoq (fe’l); navbat (ot)",
        "example": "Please turn to page forty in your English textbooks.",
        "exampleUz": "Iltimos, ingliz tili darsligingizning qirqinchi betini oching.",
        "senses": [
            {
                "definition": "to rotate around an axis or change physical direction while moving",
                "meaningUz": "burilmoq; aylanmoq",
                "example": "Turn left at the next crossroads to reach the public library.",
                "exampleUz": "Xalq kutubxonasiga yetib borish uchun keyingi chorrahada chapga buriling."
            },
            {
                "definition": "an opportunity or duty to do something in an established order among people",
                "meaningUz": "navbat",
                "example": "Now it is your turn to answer the examiner's question.",
                "exampleUz": "Endi imtihon oluvchining savoliga javob berish sizning navbatingiz."
            }
        ]
    },
    "fall": {
        "definition": "to descend rapidly from a higher to a lower level, or the autumn season",
        "meaningUz": "yiqilmoq; tushmoq (fe’l); kuz fasli (ot)",
        "example": "Dry leaves began to fall from the tall oak trees in October.",
        "exampleUz": "Oktabr oyida baland eman daraxtlaridan quruq barglar to‘kila boshladi.",
        "senses": [
            {
                "definition": "to drop down freely towards the earth under the pull of gravity",
                "meaningUz": "tushmoq; yiqilmoq",
                "example": "An apple fell from the branch right onto the soft grass.",
                "exampleUz": "Olma shoxdan to‘g‘ri yumshoq o‘t ustiga tushdi."
            },
            {
                "definition": "the season of the year between summer and winter; autumn",
                "meaningUz": "kuz fasli",
                "example": "We are planning to visit New England during the colorful fall season.",
                "exampleUz": "Biz rang-barang kuz mavsumida Yangi Angliyaga sayohat qilishni rejalashtirmoqdamiz."
            }
        ]
    },
    "cover": {
        "definition": "to place something over or upon something else to protect or hide it",
        "meaningUz": "qoplamoq; yopmoq (fe’l); muqova; qopqoq (ot)",
        "example": "Snow covered the quiet city streets under a thick white blanket.",
        "exampleUz": "Qor sokin shahar ko‘chalarini qalin oq choyshab ostida qoplab oldi.",
        "senses": [
            {
                "definition": "to lay, place, or spread something over the surface of an object",
                "meaningUz": "yopmoq; qoplamoq",
                "example": "She covered the resting baby with a warm wool blanket.",
                "exampleUz": "U uxlayotgan chaqaloqni issiq jun adyol bilan o‘rab qo‘ydi."
            },
            {
                "definition": "the outer protective binding of a book, magazine, or notebook",
                "meaningUz": "muqova",
                "example": "The vintage book featured an elegant gold-embossed leather cover.",
                "exampleUz": "Qadimiy kitob zarhal naqshli nafis charm muqovaga ega edi."
            }
        ]
    },
    "order": {
        "definition": "to request goods or food to be supplied, or an arrangement/command",
        "meaningUz": "buyurtma bermoq; buyurmoq (fe’l); tartib; buyurtma (ot)",
        "example": "We decided to order dinner from an authentic Italian restaurant tonight.",
        "exampleUz": "Biz bugun kechqurun haqiqiy italyan restoranidan kechki ovqat buyurtma qilishga qaror qildik.",
        "senses": [
            {
                "definition": "to request, ask for, or purchase goods or services from a supplier",
                "meaningUz": "buyurtma bermoq",
                "example": "I ordered three new textbooks online for the upcoming semester.",
                "exampleUz": "Men kelgusi semestr uchun onlayn tarzda uchta yangi darslik buyurtma qildim."
            },
            {
                "definition": "the methodical, systematic, or neat arrangement of things or events",
                "meaningUz": "tartib; ketma-ketlik",
                "example": "Please sort the student files in strict alphabetical order.",
                "exampleUz": "Iltimos, talabalar fayllarini qat’iy alifbo tartibida saralang."
            }
        ]
    },
    "case": {
        "definition": "a particular instance or situation, a legal lawsuit, or a protective container",
        "meaningUz": "holat; voqea; sud ishi; g‘ilof, chamadon",
        "example": "In this specific case, the medical doctor recommended gentle physiotherapy.",
        "exampleUz": "Ushbu muayyan holatda shifokor yengil fizioterapiyani tavsiya qildi.",
        "senses": [
            {
                "definition": "an individual instance, occurrence, or example of a general condition",
                "meaningUz": "holat; voqea",
                "example": "There were only a few isolated cases of the flu reported this winter.",
                "exampleUz": "Bu qishda gripp bilan kasallanishning bir necha alohida holatlari qayd etildi."
            },
            {
                "definition": "a box, sheath, or container designed to hold and protect specific items",
                "meaningUz": "g‘ilof; quti",
                "example": "He keeps his acoustic guitar safely inside a padded hard case.",
                "exampleUz": "U akustik gitarasini mustahkam g‘ilof ichida xavfsiz saqlaydi."
            }
        ]
    },
    "face": {
        "definition": "the front part of the human head, or to confront and deal with something directly",
        "meaningUz": "yuz; chehra (ot); duch kelmoq; qaramoq (fe’l)",
        "example": "A bright, joyful smile lit up her face when she saw her family.",
        "exampleUz": "Oilasini ko‘rganda uning yuzida quvnoq tabassum porlab ketdi.",
        "senses": [
            {
                "definition": "the front portion of the head extending from the forehead down to the chin",
                "meaningUz": "yuz; chehra",
                "example": "He washed his face with cold water to wake himself up.",
                "exampleUz": "U o‘ziga kelish uchun yuzini sovuq suv bilan yuvdi."
            },
            {
                "definition": "to confront, meet, or deal courageously with a difficult circumstance",
                "meaningUz": "duch kelmoq; yuzlashmoq",
                "example": "Entrepreneurs must face unexpected challenges with confidence and determination.",
                "exampleUz": "Tadbirkorlar kutilmagan qiyinchiliklarga ishonch va qat’iyat bilan yuzlashishlari kerak."
            }
        ]
    },
    "kind (type)": {
        "definition": "a group, category, or class of things or people that share similar qualities",
        "meaningUz": "tur; xil; nav",
        "example": "What kind of foreign cuisine do you enjoy eating the most?",
        "exampleUz": "Qaysi turdagi xorijiy taomlarni iste’mol qilishni eng ko‘p yoqtirasiz?"
    },
    "kind (caring)": {
        "definition": "showing warmth, friendliness, generosity, and thoughtful care for others",
        "meaningUz": "mehribon; saxiy; oqko‘ngil",
        "example": "She was always exceptionally kind and helpful to her elderly neighbors.",
        "exampleUz": "U keksa qo‘shnilariga har doim juda mehribon va yordamga tayyor edi."
    },
    "line": {
        "definition": "a continuous long narrow mark, or a row of people waiting for something",
        "meaningUz": "chiziq; qator; navbat",
        "example": "Please sign your legal signature along the dotted line at the bottom.",
        "exampleUz": "Iltimos, pastdagi nuqtali chiziq ustiga qonuniy imzoingizni qo‘ying.",
        "senses": [
            {
                "definition": "a long, thin mark traced on a surface with a pen, pencil, or instrument",
                "meaningUz": "chiziq",
                "example": "The architect drew a straight line across the blueprint.",
                "exampleUz": "Me’mor chizma bo‘ylab to‘g‘ri chiziq chizdi."
            },
            {
                "definition": "a sequence of people or vehicles positioned one behind another waiting",
                "meaningUz": "navbat; qator",
                "example": "We stood in line outside the museum for twenty minutes to buy tickets.",
                "exampleUz": "Biz chipta sotib olish uchun muzey tashqarisida yigirma daqiqa navbatda turdik."
            }
        ]
    },
    "mark": {
        "definition": "a visible sign or spot, an academic grade, or to evaluate student work",
        "meaningUz": "belgi; iz; baho (ot); baholamoq; belgilamoq (fe’l)",
        "example": "The teacher awarded her the highest possible mark on the physics essay.",
        "exampleUz": "O‘qituvchi fizika inshosi uchun unga eng yuqori bahoni qo‘ydi.",
        "senses": [
            {
                "definition": "a visible trace, spot, stain, or symbol made on a physical surface",
                "meaningUz": "belgi; dog‘; iz",
                "example": "The hot coffee mug left a dark circular mark on the wooden table.",
                "exampleUz": "Issiq qahva stakani yog‘och stol ustida qorong‘i doirasimon iz qoldirdi."
            },
            {
                "definition": "to assess, correct, and evaluate a student's assignment or examination",
                "meaningUz": "baholamoq; tekshirmoq",
                "example": "The professor stayed up late to mark fifty final examination papers.",
                "exampleUz": "Professor ellikta yakuniy imtihon qog‘ozlarini baholash uchun kechgacha o‘tirdi."
            }
        ]
    },
    "pass": {
        "definition": "to move past someone or something, or to be successful in an examination",
        "meaningUz": "o‘tib ketmoq; imtihondan o‘tmoq (fe’l); ruxsatnoma (ot)",
        "example": "She studied rigorously every evening and managed to pass her driving test.",
        "exampleUz": "U har oqshom qattiq o‘qidi va haydovchilik imtihonidan muvaffaqiyatli o‘tdi.",
        "senses": [
            {
                "definition": "to travel or move past something and proceed further ahead",
                "meaningUz": "o‘tib ketmoq; yonidan o‘tmoq",
                "example": "We watched the express train pass through the rural station at high speed.",
                "exampleUz": "Biz tezyurar poyezdning qishloq vokzali orqali yuqori tezlikda o‘tib ketishini kuzatdik."
            },
            {
                "definition": "to achieve the necessary standard and succeed in a test or examination",
                "meaningUz": "muvaffaqiyatli o‘tmoq",
                "example": "He was delighted to pass the university entrance exam with honors.",
                "exampleUz": "U universitetga kirish imtihonidan a’lo baholar bilan o‘tganidan xursand bo‘ldi."
            }
        ]
    },
    "rock (stone)": {
        "definition": "the solid mineral material forming the crust of the earth; a large stone",
        "meaningUz": "tosh; qoya",
        "example": "The climbers rested on a flat rock while admiring the mountain valley.",
        "exampleUz": "Alpinistlar tog‘ vodiysidan zavqlanib, tekis tosh ustida dam olishdi."
    },
    "rock (music)": {
        "definition": "a popular genre of modern music featuring strong rhythms, drums, and electric guitars",
        "meaningUz": "rok musiqasi",
        "example": "The young musician plays electric guitar in a local alternative rock band.",
        "exampleUz": "Yosh musiqachi mahalliy alternativ rok guruhida elektr gitarada chaladi."
    },
    "spring": {
        "definition": "the season between winter and summer, or a natural source of water",
        "meaningUz": "bahor (fasl); buloq (suv manbasi); sakramoq",
        "example": "Early spring is wonderful when colorful wildflowers start blossoming everywhere.",
        "exampleUz": "Rang-barang yovvoyi gullar har joyda gullay boshlagan erta bahor ajoyibdir.",
        "senses": [
            {
                "definition": "the season of the year after winter and before summer when temperatures rise",
                "meaningUz": "bahor",
                "example": "Trees begin to sprout fresh green leaves in early spring.",
                "exampleUz": "Daraxtlar erta bahorda yangi yashil barglar chiqara boshlaydi."
            },
            {
                "definition": "a place where pure natural water emerges from below ground to the surface",
                "meaningUz": "buloq; chashma",
                "example": "Hikers filled their water bottles from a clean natural mountain spring.",
                "exampleUz": "Sayyohlar suv idishlarini tog‘dagi toza tabiiy buloqdan to‘ldirib olishdi."
            }
        ]
    },
    "state": {
        "definition": "the condition of a person or thing, a sovereign territory, or to declare clearly",
        "meaningUz": "holat; ahvol; davlat, shtat (ot); bayon etmoq (fe’l)",
        "example": "The historic monument was preserved in an exceptionally good state of conservation.",
        "exampleUz": "Tarixiy yodgorlik nihoyatda yaxshi saqlangan holatda asrab qolingan edi.",
        "senses": [
            {
                "definition": "the physical, mental, or emotional condition of someone or something",
                "meaningUz": "holat; ahvol",
                "example": "The patient was reported to be in a stable medical state after surgery.",
                "exampleUz": "Operatsiyadan so‘ng bemorning tibbiy ahvoli barqaror ekanligi ma’lum qilindi."
            },
            {
                "definition": "a politically organized community or geographic area under a unified government",
                "meaningUz": "davlat; shtat",
                "example": "Texas is the second-largest state in the United States by land area.",
                "exampleUz": "Texas hududi bo‘yicha AQShning ikkinchi eng katta shtatidir."
            },
            {
                "definition": "to express or announce something definitely and clearly in speech or text",
                "meaningUz": "bayon etmoq; ta’kidlamoq",
                "example": "Please state your full name, occupation, and current address.",
                "exampleUz": "Iltimos, to‘liq ismingiz, kasbingiz va hozirgi manzilingizni bayon eting."
            }
        ]
    },
    "point": {
        "definition": "an idea or argument, a sharp end, or to direct attention by extending a finger",
        "meaningUz": "fikr; ma’no; nuqta (ot); ko‘rsatmoq; ishora qilmoq (fe’l)",
        "example": "The speaker raised an insightful point during the economics conference.",
        "exampleUz": "Notiq iqtisodiyot anjumanida chuqur ma’noli fikrni o‘rtaga tashladi.",
        "senses": [
            {
                "definition": "an opinion, argument, or essential idea that someone tries to explain",
                "meaningUz": "fikr; muhim jihat",
                "example": "I completely understand the main point you are trying to make.",
                "exampleUz": "Men siz aytmoqchi bo‘lgan asosiy fikrni to‘liq tushunaman."
            },
            {
                "definition": "to extend a finger or an object towards something to draw attention to it",
                "meaningUz": "ko‘rsatmoq; ishora qilmoq",
                "example": "The tour guide pointed at the ancient castle standing high on the hill.",
                "exampleUz": "Gid tepalikda qad ko‘targan qadimiy qasrga barmog‘i bilan ishora qildi."
            }
        ]
    },
    "can1": {
        "definition": "used to indicate ability, possibility, or permission to perform an action",
        "meaningUz": "qila olmoq; qo‘lidan kelmoq (modal fe’l)",
        "example": "She can speak four different languages fluently.",
        "exampleUz": "U to‘rtta turli tilda ravon gaplasha oladi."
    },
    "can2": {
        "definition": "a cylindrical metal container in which food, beverages, or chemicals are preserved",
        "meaningUz": "konserva bankasi; metall quti",
        "example": "He bought a can of tomato soup and two cans of sparkling soda.",
        "exampleUz": "U bir banka pomidor sho‘rvasi va ikkita gazlangan ichimlik metall qutisini sotib oldi."
    },
    "close1": {
        "definition": "to shut an opening or cover, or to bring something to an end",
        "meaningUz": "yopmoq; berkilmoq",
        "example": "Please close the front door so the cold winter draft does not enter.",
        "exampleUz": "Iltimos, sovuq qish shamoli kirmasligi uchun old eshikni yoping."
    },
    "close2": {
        "definition": "situated a short distance away in space or time; near; intimate",
        "meaningUz": "yaqin; yonma-yon",
        "example": "The post office is located very close to our neighborhood school.",
        "exampleUz": "Pochta bo‘limi bizning mahalladagi maktabga juda yaqin joylashgan."
    },
    "bear (animal)": {
        "definition": "a large wild mammal with heavy fur, sharp curved claws, and powerful limbs",
        "meaningUz": "ayiq",
        "example": "The wild grizzly bear caught fresh salmon in the fast-flowing Alaskan stream.",
        "exampleUz": "Yovvoyi ayiq Alyaskaning tez oqar soyidan yangi losos balig‘ini tutib oldi."
    },
    "bear (deal with)": {
        "definition": "to endure, tolerate, or carry on under difficult or painful conditions",
        "meaningUz": "chidamoq; bardosh bermoq; toqat qilmoq",
        "example": "She could hardly bear the pain after spraining her ankle during gymnastics.",
        "exampleUz": "Gimnastika mashg‘ulotida to‘pig‘ini qayirib olgach, u og‘riqqa arang bardosh berdi."
    },
    "tear1": {
        "definition": "to pull or rip something apart into pieces with force",
        "meaningUz": "yirtmoq; yirtilmoq",
        "example": "He accidentally tore his sleeve when it caught on an exposed iron nail.",
        "exampleUz": "Ochiq temir mixga ilinib qolganida, u tasodifan ko‘ylagining yengini yirtib oldi."
    },
    "tear2": {
        "definition": "a drop of salty liquid secreted by the eyes in response to sadness or irritation",
        "meaningUz": "ko‘z yoshi",
        "example": "Tears of joy streamed down her cheeks when she saw her daughter graduate.",
        "exampleUz": "Qizining o‘qishni bitirganini ko‘rganda uning yuzidan quvonch ko‘z yoshlari oqdi."
    },
    "wind1": {
        "definition": "a natural current of air moving horizontally across the earth's surface",
        "meaningUz": "shamol",
        "example": "A strong westerly wind blew dark rain clouds across the evening sky.",
        "exampleUz": "Kuchli g‘arbiy shamol oqshom osmoni bo‘ylab qora yomg‘ir bulutlarini haydadi."
    },
    "wind2": {
        "definition": "to twist, coil, or turn something around a central axis or object",
        "meaningUz": "o‘ramoq; buramoq; chulg‘amoq",
        "example": "Remember to wind the vintage mechanical clock every Sunday morning.",
        "exampleUz": "Har yakshanba kuni ertalab qadimiy mexanik soatni burab qo‘yishni unutmang."
    },
    "mine (belongs to me)": {
        "definition": "used to refer to the thing or things that belong to or are associated with me",
        "meaningUz": "meniki",
        "example": "This black umbrella is mine, while the red one belongs to Sarah.",
        "exampleUz": "Bu qora soyabon meniki, qizili esa Saraga tegishli."
    },
    "mine (hole in the ground)": {
        "definition": "a deep hole or tunnel excavated underground to extract coal, minerals, or gems",
        "meaningUz": "shaxta; kon",
        "example": "Generations of miners worked in the local underground copper mine.",
        "exampleUz": "Mahalliy yer osti mis konida konchilarning bir necha avlodi ishlagan."
    },
    "race (competition)": {
        "definition": "a sports competition to see who or what is the fastest runner, driver, etc.",
        "meaningUz": "poyga; yugurish musobaqasi",
        "example": "The champion runner crossed the finish line first in the marathon race.",
        "exampleUz": "Chempion yuguruvchi marafon poygasida birinchi bo‘lib marraga yetib keldi."
    },
    "race (of people)": {
        "definition": "a major group into which humans can be divided according to shared physical characteristics",
        "meaningUz": "irq; milliy guruh",
        "example": "People of every race and background should be treated with dignity and equality.",
        "exampleUz": "Har bir irq va millatga mansub odamlarga hurmat va tenglik bilan munosabatda bo‘lish kerak."
    },
    "rest (remaining part)": {
        "definition": "the remaining part or quantity of people or things that haven't been mentioned",
        "meaningUz": "qolgan qismi; qolganlar",
        "example": "I finished half of the assignment today and will complete the rest tomorrow.",
        "exampleUz": "Men topshiriqning yarmini bugun tugatdim va qolgan qismini ertaga yakunlayman."
    },
    "rest (sleep/relax)": {
        "definition": "to cease work or movement in order to relax, refresh, or regain strength",
        "meaningUz": "dam olmoq; hordiq chiqarmoq",
        "example": "After walking uphill for three hours, they stopped beneath an oak tree to rest.",
        "exampleUz": "Uch soat davomida tepalikka chiqqandan so‘ng, ular dam olish uchun eman daraxti tagida to‘xtashdi."
    },
    "ring1": {
        "definition": "a circular band of precious metal, such as gold or silver, worn on a finger",
        "meaningUz": "uzuk",
        "example": "He placed a diamond engagement ring gently onto her finger.",
        "exampleUz": "U uning barmog‘iga olmosli unashtiruv uzugini muloyimlik bilan taqib qo‘ydi."
    },
    "ring2": {
        "definition": "to make a clear resonant metallic sound, or to telephone someone",
        "meaningUz": "jiringlamoq; qo‘ng‘iroq qilmoq",
        "example": "I will ring you back as soon as my afternoon business meeting finishes.",
        "exampleUz": "Tushdan keyingi ish uchrashuvim tugashi bilanoq sizga qo‘ng‘iroq qilaman."
    },
    "point": {
        "definition": "an opinion, idea, or fact that someone expresses in a discussion",
        "meaningUz": "fikr; ma'no",
        "example": "You made a very important point during the team meeting today.",
        "exampleUz": "Bugungi jamoa yig‘ilishida siz juda muhim fikr bildirdingiz.",
        "senses": [
            {
                "definition": "an idea or opinion expressed in a discussion or debate",
                "meaningUz": "fikr; mulohaza",
                "example": "I understand your point, but we must consider the budget.",
                "exampleUz": "Fikringizni tushunaman, lekin byudjetni ham hisobga olishimiz kerak."
            },
            {
                "definition": "to direct someone's attention towards something by extending a finger",
                "meaningUz": "ko'rsatmoq; ishora qilmoq",
                "example": "He pointed at the distant mountain peak.",
                "exampleUz": "U uzoqdagi tog‘ cho‘qqisini barmog‘i bilan ko‘rsatdi."
            }
        ]
    },
    "case": {
        "definition": "a particular situation, instance, or example of something happening",
        "meaningUz": "holat; vaziyat",
        "example": "In this specific case, the manager decided to make an exception to the policy.",
        "exampleUz": "Ushbu muayyan holatda menejer qoidadan istisno qilishga qaror qildi.",
        "senses": [
            {
                "definition": "a particular situation or occurrence of something",
                "meaningUz": "holat; voqea",
                "example": "That was an unusual case that required special attention.",
                "exampleUz": "Bu alohida e'tiborni talab qiladigan g‘ayrioddiy holat edi."
            },
            {
                "definition": "a container or box designed to hold or protect a specific item",
                "meaningUz": "g'ilof; quti; chamadon",
                "example": "She placed her sunglasses securely in a hard leather case.",
                "exampleUz": "U quyoshdan saqlovchi ko‘zoynagini qattiq charm g‘ilofga xavfsiz joylashtirdi."
            }
        ]
    },
    "face": {
        "definition": "the front part of the human head from the forehead to the chin",
        "meaningUz": "yuz; chehra",
        "example": "A bright warm smile spread across her happy face.",
        "exampleUz": "Uning baxtli yuzida samimiy iliq tabassum paydo bo‘ldi.",
        "senses": [
            {
                "definition": "the front part of the head including the eyes, nose, and mouth",
                "meaningUz": "yuz; bet",
                "example": "He washed his face with cold water to wake up.",
                "exampleUz": "U uyg‘onish uchun yuzini sovuq suv bilan yuvdi."
            },
            {
                "definition": "to look or turn towards a particular direction or to confront a problem",
                "meaningUz": "qaramoq; yuzlanmoq",
                "example": "The classroom windows face towards the peaceful garden.",
                "exampleUz": "Sinf xonasi derazalari sokin bog‘ tomon qaragan."
            }
        ]
    },
    "kind": {
        "definition": "a group with similar characteristics; a type, category, or variety",
        "meaningUz": "tur; xil",
        "example": "What kind of foreign literature do you prefer reading in your spare time?",
        "exampleUz": "Bo‘sh vaqtingizda qanday turdagi xorijiy adabiyotlarni o‘qishni afzal ko‘rasiz?",
        "senses": [
            {
                "definition": "a category of people or things having common characteristics",
                "meaningUz": "tur; xil",
                "example": "We sell many different kinds of fresh organic fruits.",
                "exampleUz": "Biz ko‘plab turli xil yangi organik mevalarni sotamiz."
            },
            {
                "definition": "having or showing a friendly, generous, and considerate nature",
                "meaningUz": "mehribon; saxiy; xayrixoh",
                "example": "It was very kind of the stranger to help us carry our heavy bags.",
                "exampleUz": "Bizga og‘ir sumkalarimizni ko‘tarishga yordam bergan begona inson juda saxiy edi."
            }
        ]
    },
    "line": {
        "definition": "a long, narrow mark or band on a surface",
        "meaningUz": "chiziq; yo'l",
        "example": "Please sign your signature on the dotted line at the bottom of the contract.",
        "exampleUz": "Iltimos, shartnomaning pastki qismidagi nuqtali chiziqqa imzo cheking.",
        "senses": [
            {
                "definition": "a continuous mark made on a surface by a pen, pencil, or brush",
                "meaningUz": "chiziq",
                "example": "The teacher drew a straight line across the chalkboard.",
                "exampleUz": "O‘qituvchi doskaga to‘g‘ri chiziq chizdi."
            },
            {
                "definition": "a row of people or vehicles waiting for their turn",
                "meaningUz": "navbat; qator",
                "example": "Customers waited patiently in a long line outside the store.",
                "exampleUz": "Mijozlar do‘kon tashqarisida uzoq navbatda sabr bilan kutishdi."
            }
        ]
    },
    "mark": {
        "definition": "a visible impression, trace, or spot on a surface",
        "meaningUz": "belgi; dog'; iz",
        "example": "There was a persistent water mark left on the wooden tabletop.",
        "exampleUz": "Yog‘och stol ustida doimiy suv dog‘i qolgan edi.",
        "senses": [
            {
                "definition": "a small area on a surface having a different color or texture",
                "meaningUz": "dog'; iz",
                "example": "Wipe away that dark pencil mark from the wall.",
                "exampleUz": "Devordagi qora qalam izini artib tashlang."
            },
            {
                "definition": "a number or letter given to evaluate a student's performance",
                "meaningUz": "baho; ball",
                "example": "She received the highest mark on the chemistry examination.",
                "exampleUz": "U kimyo imtihonida eng yuqori bahoni oldi."
            }
        ]
    },
    "pass": {
        "definition": "to move past or beyond someone or something in space or time",
        "meaningUz": "o'tmoq; yonidan o'tib ketmoq",
        "example": "We watched several freight trains pass through the rural station.",
        "exampleUz": "Biz qishloq vokzalidan bir nechta yuk poyezdlarining o‘tib ketishini kuzatdik.",
        "senses": [
            {
                "definition": "to move past someone or something while travelling",
                "meaningUz": "o'tmoq; yonidan o'tmoq",
                "example": "Cars pass through the tunnel every few seconds.",
                "exampleUz": "Har bir necha soniyada tunneldan mashinalar o‘tadi."
            },
            {
                "definition": "to successfully achieve the required standard in an exam or test",
                "meaningUz": "muvaffaqiyatli topshirmoq; o'tmoq",
                "example": "She worked diligently every evening to pass her university entrance exam.",
                "exampleUz": "U universitetga kirish imtihonidan o‘tish uchun har oqshom tirishqoqlik bilan o‘qidi."
            }
        ]
    },
    "rock": {
        "definition": "the solid mineral material forming part of the surface of the earth",
        "meaningUz": "tosh; qoya",
        "example": "Hikers climbed over large granite rocks to reach the mountain summit.",
        "exampleUz": "Sayyohlar tog‘ cho‘qqisiga chiqish uchun katta granit qoyalardan oshib o‘tishdi.",
        "senses": [
            {
                "definition": "the hard solid material found in the earth's crust",
                "meaningUz": "tosh; qoya",
                "example": "A huge rock rolled down the steep cliff after the rain.",
                "exampleUz": "Yomg‘irdan so‘ng tik qoyadan ulkan tosh pastga dumalab tushdi."
            },
            {
                "definition": "to move rhythmically back and forth or from side to side",
                "meaningUz": "tebranmoq; tebratmoq",
                "example": "The gentle ocean waves rocked the sailboat peacefully.",
                "exampleUz": "Mayin okean to‘lqinlari yelkanli qayiqni sokin tebratdi."
            }
        ]
    }
}
