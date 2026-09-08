# -*- coding: utf-8 -*-
"""Onboarding, paywall, app shell, tabs, toasts. Order: he, en, fr, ru, ar"""

APP = {

# ---------- onboarding ----------
'o.step':        ('שלב {n} מתוך {t}', 'Step {n} of {t}', 'Étape {n} sur {t}', 'Шаг {n} из {t}', 'الخطوة {n} من {t}'),
'o.1.t':         ('נעים להכיר', 'Nice to meet you', 'Enchanté', 'Приятно познакомиться', 'تشرفنا'),
'o.1.s':         ('שם, גיל ומייל — כדי לשמור את ההתקדמות שלך.',
                  'Name, age and email — so your progress is saved.',
                  'Nom, âge et e-mail — pour sauvegarder ta progression.',
                  'Имя, возраст и почта — чтобы сохранять прогресс.',
                  'الاسم والعمر والبريد — لحفظ تقدّمك.'),
'o.age':         ('גיל', 'Age', 'Âge', 'Возраст', 'العمر'),
'o.age.ph':      ('הגיל שלך', 'Your age', 'Ton âge', 'Твой возраст', 'عمرك'),
'o.iam':        ('אני', 'I am', 'Je suis', 'Я', 'أنا'),
'o.iam.boy':    ('בן', 'A boy', 'Un garçon', 'Парень', 'ولد'),
'o.iam.girl':   ('בת', 'A girl', 'Une fille', 'Девушка', 'بنت'),
'o.iam.na':     ('מעדיף לא לומר', 'Rather not say', 'Je préfère ne pas dire',
                 'Предпочитаю не говорить', 'أفضّل عدم القول'),
'o.iam.note':   ('זה רק קובע את צבע ברירת המחדל. אפשר לשנות אותו בכל רגע למעלה.',
                 'This only sets your default colour. You can change it any time up top.',
                 'Cela ne fixe que ta couleur par défaut. Modifiable à tout moment en haut.',
                 'Это задаёт только цвет по умолчанию. Его можно сменить в любой момент сверху.',
                 'هذا يحدد لونك الافتراضي فقط. يمكنك تغييره في أي وقت من الأعلى.'),

'th.light':     ('מצב בהיר', 'Light mode', 'Mode clair', 'Светлая тема', 'الوضع الفاتح'),
'th.dark':      ('מצב כהה', 'Dark mode', 'Mode sombre', 'Тёмная тема', 'الوضع الداكن'),
'th.acc.flame': ('להבה', 'Flame', 'Flamme', 'Пламя', 'لهب'),
'th.acc.bloom': ('פריחה', 'Bloom', 'Éclat', 'Цветение', 'إزهار'),
'th.acc.mint':  ('מנטה', 'Mint', 'Menthe', 'Мята', 'نعناع'),

'o.2.t':         ('מה מעניין אותך?', 'What are you into?', 'Qu\'est-ce qui t\'intéresse ?', 'Что тебе интересно?', 'ما الذي يهمك؟'),
'o.2.s':         ('{בחר|בחרי} תחומים, {והוסף|והוסיפי} משלך אם חסר משהו.',
                  'Pick your areas, and add your own if something is missing.',
                  'Choisis tes domaines, et ajoute les tiens si besoin.',
                  'Выбери направления и добавь свои, если чего-то не хватает.',
                  '{اختر|اختاري} مجالاتك، {وأضف|وأضيفي} ما ينقص.'),
'o.2.custom':    ('תחום משלך', 'Your own area', 'Ton propre domaine', 'Своё направление', 'مجال خاص بك'),
'o.2.custom.ph': ('משהו שלא ברשימה...', 'Something not on the list…', 'Quelque chose qui n\'y est pas…', 'Чего нет в списке…', 'شيء ليس في القائمة…'),

'o.3.t':         ('מה קל ומה קשה?', 'What is easy, what is hard?', 'Facile ou difficile ?', 'Что легко, что трудно?', 'ما السهل وما الصعب؟'),

'o.time.15':     ('15 דקות', '15 minutes', '15 minutes', '15 минут', '15 دقيقة'),
'o.time.30':     ('30 דקות', '30 minutes', '30 minutes', '30 минут', '30 دقيقة'),
'o.time.45':     ('45+ דקות', '45+ minutes', '45+ minutes', '45+ минут', '45+ دقيقة'),

'o.5.t':         ('ספורט', 'Training', 'Sport', 'Спорт', 'الرياضة'),
'o.5.goal':      ('המטרה שלך באימון', 'What you train for', 'Ton objectif sportif', 'Твоя цель в тренировках', 'هدفك من التمرين'),
'o.5.exp':       ('הניסיון שלך', 'Your experience', 'Ton expérience', 'Твой опыт', 'خبرتك'),

'o.6.t':         ('טיפוח', 'Skincare', 'Soin de la peau', 'Уход за кожей', 'العناية بالبشرة'),
'o.6.skin':      ('סוג העור שלך', 'Your skin type', 'Ton type de peau', 'Тип твоей кожи', 'نوع بشرتك'),

# ---------- paywall (onboarding step 9) ----------
'o.9.t':         ('התוכנית שלך מוכנה', 'Your plan is ready', 'Ton plan est prêt', 'Твой план готов', 'خطتك جاهزة'),
'o.9.s':         ('בנינו אותה לפי הגיל, הזמן והמטרות שהזנת. 14 הימים הראשונים חינם.',
                  'We built it from the age, time and goals you entered. The first 14 days are free.',
                  'Construit selon ton âge, ton temps et tes objectifs. Les 14 premiers jours sont gratuits.',
                  'Мы построили его по твоему возрасту, времени и целям. Первые 14 дней бесплатны.',
                  'بنيناها حسب عمرك ووقتك وأهدافك. أول 14 يوماً مجانية.'),
'o.9.built1':    ('{n} קטגוריות יומיות', '{n} daily categories', '{n} catégories quotidiennes', '{n} ежедневных категорий', '{n} فئات يومية'),
'o.9.built2':    ('תוכנית אימונים ל-7 ימים', 'A 7-day training plan', 'Un programme de 7 jours', 'План тренировок на 7 дней', 'خطة تمارين لسبعة أيام'),
'o.9.built3':    ('{n} מטרות מפורקות לצעדים', '{n} goals broken into steps', '{n} objectifs découpés en étapes', '{n} целей, разбитых на шаги', '{n} أهداف مقسّمة إلى خطوات'),
'o.9.later':     ('אולי אחר כך', 'Maybe later', 'Plus tard', 'Может быть, позже', 'ربما لاحقاً'),
'o.9.laternote': ('נכנסת עם הניסיון. אפשר לשדרג מתי שתרצה.',
                  'You are in on the trial. Upgrade whenever you want.',
                  'Tu es dans l\'essai. Tu pourras passer à l\'offre payante quand tu veux.',
                  'Ты на пробном периоде. Обновиться можно в любой момент.',
                  'أنت في التجربة. يمكنك الترقية متى شئت.'),

# ---------- checkout stub ----------

# ---------- trial strip ----------
'trial.left':    ('נשארו {n} ימי ניסיון', '{n} trial days left', 'Il reste {n} jours d\'essai', 'Осталось {n} дней пробного периода', 'بقي {n} يوماً من التجربة'),
'trial.last':    ('היום האחרון בניסיון', 'Last day of your trial', 'Dernier jour d\'essai', 'Последний день пробного периода', 'آخر يوم في التجربة'),
'trial.over':    ('הניסיון הסתיים', 'Your trial has ended', 'Ton essai est terminé', 'Пробный период закончился', 'انتهت التجربة'),
'trial.cta':     ('שדרג', 'Upgrade', 'Passer au payant', 'Улучшить', 'ترقية'),

# ---------- app shell ----------
'a.greet':       ('היי {name}', 'Hey {name}', 'Salut {name}', 'Привет, {name}', 'أهلاً {name}'),
'a.greet.anon':  ('{אלוף|אלופה}', 'champ', '{champion|championne}', '{чемпион|чемпионка}', '{بطل|بطلة}'),
'a.level':       ('רמה', 'Level', 'Niveau', 'Уровень', 'المستوى'),
'a.tab.goals':   ('מטרות', 'Goals', 'Objectifs', 'Цели', 'الأهداف'),
'a.tab.body':    ('גוף', 'Body', 'Corps', 'Тело', 'الجسم'),

# ---------- home ----------
'h.ring.t':      ('המעגל של היום', 'Today\'s ring', 'Le cercle du jour', 'Круг дня', 'دائرة اليوم'),
'h.ring.s':      ('כל משימה נסגרת בתמונה. בלי הוכחה אין וי. פספסת אחת? ממשיכים.',
                  'Every task closes with a photo. No proof, no check. Missed one? Keep going.',
                  'Chaque tâche se ferme avec une photo. Pas de preuve, pas de validation. Raté ? On continue.',
                  'Каждая задача закрывается фото. Нет доказательства — нет галочки. Пропустил? Идём дальше.',
                  'كل مهمة تُغلق بصورة. لا إثبات، لا علامة. فاتتك واحدة؟ نكمل.'),
'h.done':        ('הושלם', 'Done', 'Fait', 'Готово', 'مكتمل'),
'h.streak':      ('רצף', 'Streak', 'Série', 'Серия', 'سلسلة'),
'h.points':      ('נקודות', 'Points', 'Points', 'Очки', 'نقاط'),
'h.tasks':       ('משימות', 'Tasks', 'Tâches', 'Задачи', 'المهام'),
'h.insight':     ('תובנה', 'Insight', 'Éclairage', 'Инсайт', 'ملاحظة'),
'h.empty':       ('אין עוד משימות כאן. {הוסף|הוסיפי} אחת.', 'No tasks here yet. Add one.', 'Aucune tâche ici. Ajoutes-en une.', 'Здесь пока нет задач. Добавь одну.', 'لا مهام هنا بعد. {أضف|أضيفي} واحدة.'),
'h.add.ph':      ('משימה משלך', 'Your own task', 'Ta propre tâche', 'Своя задача', 'مهمتك الخاصة'),
'h.add.min':     ('דק׳', 'min', 'min', 'мин', 'د'),

# ---------- goals ----------
'g.t':           ('המטרות שלי', 'My goals', 'Mes objectifs', 'Мои цели', 'أهدافي'),
'g.s':           ('יעד נבנה ממה שבא לך לשפר, ומתחיל להיספר רק כשלוחצים "התחל".',
                  'A target is built from what you want to improve, and only starts counting when you press "start".',
                  'Un objectif se construit à partir de ce que tu veux améliorer, et ne compte qu\'une fois que tu appuies sur « lancer ».',
                  'Цель строится из того, что ты хочешь улучшить, и начинает считаться только после нажатия «начать».',
                  'يُبنى الهدف ممّا تريد تحسينه، ولا يبدأ العدّ إلا عند الضغط على «ابدأ».'),
'g.new.ph':      ('מטרה חדשה', 'A new goal', 'Nouvel objectif', 'Новая цель', 'هدف جديد'),
'g.step.ph':     ('צעד משלך', 'Your own step', 'Ton étape', 'Свой шаг', 'خطوة خاصة بك'),

# ---------- week ----------
'w.t':           ('הטבלה השבועית', 'The weekly grid', 'Le tableau de la semaine', 'Недельная таблица', 'الجدول الأسبوعي'),
'w.s':           ('{סמן|סמני} כל יום שבו ביצעת. היעד הוא כמה ימים בשבוע, לא כל יום.',
                  'Mark every day you did it. The target is a number of days a week, not every day.',
                  'Coche chaque jour réalisé. L\'objectif est un nombre de jours, pas tous les jours.',
                  'Отмечай каждый выполненный день. Цель — сколько дней в неделю, а не каждый день.',
                  '{ضع|ضعي} علامة على كل يوم نفّذته. الهدف عدد أيام في الأسبوع، لا كل يوم.'),
'w.met':         ('הושגו', 'Met', 'Atteints', 'Достигнуто', 'تحقق'),
'w.reset':       ('שבוע חדש', 'New week', 'Nouvelle semaine', 'Новая неделя', 'أسبوع جديد'),
'w.col.mission': ('משימה', 'Mission', 'Mission', 'Задача', 'مهمة'),
'w.col.status':  ('סטטוס', 'Status', 'Statut', 'Статус', 'الحالة'),
'w.empty':       ('אין משימות שבועיות. {הוסף|הוסיפי} אחת למטה.', 'No weekly missions yet. Add one below.', 'Aucune mission hebdo. Ajoutes-en une.', 'Недельных задач нет. Добавь одну ниже.', 'لا مهام أسبوعية. {أضف|أضيفي} واحدة بالأسفل.'),
'w.new.ph':      ('משימה שבועית', 'Weekly mission', 'Mission hebdomadaire', 'Недельная задача', 'مهمة أسبوعية'),
'w.target':      ('יעד', 'Target', 'Objectif', 'Цель', 'الهدف'),
'w.st.win':      ('הושג', 'Met', 'Atteint', 'Достигнуто', 'تحقق'),
'w.st.close':    ('כמעט', 'Close', 'Presque', 'Почти', 'تقريباً'),
'w.st.going':    ('בתהליך', 'In progress', 'En cours', 'В процессе', 'قيد التنفيذ'),
'w.st.none':     ('עוד לא התחיל', 'Not started', 'Pas commencé', 'Не начато', 'لم يبدأ'),
'w.rev.t':       ('סיכום שבוע', 'Week review', 'Bilan de la semaine', 'Итоги недели', 'مراجعة الأسبوع'),
'w.rev.s':       ('בוא נראה כמה יעדים סגרת.', 'Let us see how many targets you closed.', 'Voyons combien d\'objectifs tu as atteints.', 'Посмотрим, сколько целей ты закрыл.', 'لنرَ كم هدفاً أغلقت.'),
'w.rev.btn':     ('סיכום השבוע', 'Review week', 'Faire le bilan', 'Подвести итоги', 'راجع الأسبوع'),
'w.rev.perfect': ('שבוע מושלם.', 'A perfect week.', 'Une semaine parfaite.', 'Идеальная неделя.', 'أسبوع مثالي.'),
'w.rev.strong':  ('שבוע חזק.', 'A strong week.', 'Une bonne semaine.', 'Сильная неделя.', 'أسبوع قوي.'),
'w.rev.start':   ('כל התחלה נחשבת.', 'Every start counts.', 'Chaque début compte.', 'Любое начало важно.', 'كل بداية تُحتسب.'),

# ---------- body ----------
'bd.hy.t':       ('בריאות והיגיינה', 'Health and hygiene', 'Santé et hygiène', 'Здоровье и гигиена', 'الصحة والنظافة'),
'bd.hy.s':       ('הרגלים יומיים שקל לשכוח.', 'Daily habits that are easy to forget.', 'Des habitudes quotidiennes vite oubliées.', 'Ежедневные привычки, о которых легко забыть.', 'عادات يومية يسهل نسيانها.'),

# ---------- why it works ----------
'y.t':           ('למה זה עובד', 'Why this works', 'Pourquoi ça marche', 'Почему это работает', 'لماذا ينجح هذا'),
'y.s':           ('כל מנגנון באפליקציה נשען על מחקר קיים. הנה מה ועל מה.',
                  'Every mechanism here rests on existing research. Here is what and on what.',
                  'Chaque mécanisme repose sur des recherches existantes. Voici lesquelles.',
                  'Каждый механизм здесь опирается на существующие исследования. Вот на какие.',
                  'كل آلية هنا تستند إلى بحث قائم. إليك ماذا وعلى ماذا.'),
'y.where':       ('איפה באפליקציה', 'Where in the app', 'Où dans l\'app', 'Где в приложении', 'أين في التطبيق'),

# ---------- camera ----------
'cam.t':         ('צילום הוכחה', 'Capture proof', 'Prends la preuve', 'Сделай доказательство', 'التقط الإثبات'),

# ---------- toasts ----------
't.agerange':    ('{כתוב|כתבי} גיל בין 13 ל-120 כדי להמשיך',
                  'Enter an age between 13 and 120 to continue',
                  'Saisis un âge entre 13 et 120 pour continuer',
                  'Введи возраст от 13 до 120, чтобы продолжить',
                  '{أدخل|أدخلي} عمراً بين 13 و120 للمتابعة'),
't.pickarea':    ('{בחר|בחרי} לפחות תחום אחד', 'Pick at least one area', 'Choisis au moins un domaine', 'Выбери хотя бы одно направление', '{اختر|اختاري} مجالاً واحداً على الأقل'),
't.added':       ('נוסף: {x}', 'Added: {x}', 'Ajouté : {x}', 'Добавлено: {x}', 'أُضيف: {x}'),
't.goaladded':   ('מטרה נוספה ופורקה לצעדים', 'Goal added and broken into steps', 'Objectif ajouté et découpé', 'Цель добавлена и разбита на шаги', 'أُضيف الهدف وقُسّم إلى خطوات'),
't.writegoal':   ('{כתוב|כתבי} מטרה קודם', 'Write a goal first', 'Écris d\'abord un objectif', 'Сначала напиши цель', '{اكتب|اكتبي} هدفاً أولاً'),
't.newweek':     ('שבוע חדש התחיל', 'A new week has started', 'Nouvelle semaine lancée', 'Началась новая неделя', 'بدأ أسبوع جديد'),
't.timerdone':   ('הטיימר נגמר', 'Timer finished', 'Minuteur terminé', 'Таймер закончился', 'انتهى المؤقت'),
't.pts':         ('+{n} נקודות', '+{n} points', '+{n} points', '+{n} очков', '+{n} نقاط'),
't.step':        ('צעד קדימה', 'A step forward', 'Un pas en avant', 'Шаг вперёд', 'خطوة إلى الأمام'),
't.proof':       ('הוכחה נשמרה', 'Proof saved', 'Preuve enregistrée', 'Доказательство сохранено', 'حُفظ الإثبات'),

# ---------- praise (random on completion) ----------
'p.1':           ('זה נחשב.', 'That counts.', 'Ça compte.', 'Это засчитано.', 'هذا يُحتسب.'),
'p.2':           ('עוד אחד בכיס.', 'One more in the bag.', 'Un de plus.', 'Ещё один в копилку.', 'واحدة أخرى في الجيب.'),
'p.3':           ('ככה נבנה רצף.', 'This is how a streak gets built.', 'C\'est comme ça qu\'on bâtit une série.', 'Так и строится серия.', 'هكذا تُبنى السلسلة.'),
'p.4':           ('החלטת, ועשית.', 'You decided, and you did it.', 'Tu as décidé, et tu l\'as fait.', 'Решил — и сделал.', 'قررت، وفعلت.'),
'p.5':           ('קטן, אבל אמיתי.', 'Small, but real.', 'Petit, mais réel.', 'Мало, но по-настоящему.', 'صغير، لكنه حقيقي.'),
}
