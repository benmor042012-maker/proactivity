# -*- coding: utf-8 -*-
"""Pro, licences, backup, calendar, install and the progress trend.

Entries are 'key': (he, en, fr, ru, ar). A {masculine|feminine} segment is
resolved by t() before placeholders are filled; most of these lines are written
to work for anyone, which is why few of them carry one.
"""
PRO = {

# ---------- the tier ----------
'pro.lock.t':     ('זה נמצא בפרו',
                   'This one is in Pro',
                   'Ça fait partie de Pro',
                   'Это входит в Pro',
                   'هذه الميزة ضمن Pro'),
'pro.lock.cta':   ('לראות מה יש בפרו', 'See what Pro includes', 'Voir ce que Pro contient',
                   'Посмотреть, что входит в Pro', 'اطّلع على ما يشمله Pro'),
'pro.have':       ('יש לי כבר קוד', 'I already have a key', 'J\'ai déjà une clé',
                   'У меня уже есть ключ', 'لديّ مفتاح بالفعل'),
'pro.f.body':     ('טאב הגוף — תוכנית אימונים לפי גיל ורמה, שגרת טיפוח לפי סוג עור, '
                   'והמקרר שמציע מתכון ממה שיש בבית.',
                   'The Body tab — a workout plan by age and level, a skincare routine by skin '
                   'type, and the fridge that suggests a recipe from what you already have.',
                   'L\'onglet Corps — un programme sportif selon l\'âge et le niveau, une routine '
                   'soin selon le type de peau, et le frigo qui propose une recette avec ce que tu as.',
                   'Вкладка «Тело» — план тренировок по возрасту и уровню, уход за кожей по её типу '
                   'и холодильник, который предлагает рецепт из того, что уже есть дома.',
                   'تبويب الجسم — خطة تمارين حسب العمر والمستوى، وروتين عناية حسب نوع البشرة، '
                   'والثلاجة التي تقترح وصفة مما هو موجود في البيت.'),
'pro.f.trend':    ('הגרף שמראה איך מדד הפרואקטיביות שלך זז לאורך הזמן, שאלון אחרי שאלון.',
                   'The chart that shows how your proactivity score has moved over time, '
                   'check-in after check-in.',
                   'Le graphique qui montre comment ton indice de proactivité a bougé dans le temps, '
                   'bilan après bilan.',
                   'График, который показывает, как менялся твой индекс проактивности — '
                   'от одной проверки к другой.',
                   'الرسم الذي يُظهر كيف تحرّك مؤشر المبادرة لديك مع الوقت، مراجعة بعد مراجعة.'),
'pro.goalmax':    ('{n} יעדים פעילים זה המקסימום בחינם. אפשר לסיים יעד קיים, או לפתוח פרו.',
                   '{n} active targets is the free maximum. Finish one, or open Pro.',
                   '{n} objectifs actifs, c\'est le maximum en gratuit. Termines-en un, ou passe à Pro.',
                   '{n} активные цели — максимум на бесплатном тарифе. Заверши одну или открой Pro.',
                   '{n} أهداف نشطة هي الحد الأقصى في النسخة المجانية. أنهِ هدفاً، أو افتح Pro.'),

# ---------- state ----------
'pro.state.pro':     ('פרו פעיל.', 'Pro is active.', 'Pro est actif.',
                      'Pro активен.', 'Pro مُفعّل.'),
'pro.state.pro.exp': ('פרו פעיל עד {d}.', 'Pro is active until {d}.', 'Pro est actif jusqu\'au {d}.',
                      'Pro активен до {d}.', 'Pro مُفعّل حتى {d}.'),
'pro.state.founder': ('הכל פתוח אצלך — היית כאן לפני שפרו נולד, וזה נשאר ככה.',
                      'Everything is open for you — you were here before Pro existed, and that stays.',
                      'Tout est ouvert pour toi — tu étais là avant Pro, et ça ne change pas.',
                      'У тебя открыто всё — ты был здесь до появления Pro, и так и останется.',
                      'كل شيء مفتوح لك — كنت هنا قبل وجود Pro، وسيبقى الأمر كذلك.'),
'pro.state.trial':   ('ניסיון — נשארו {n} ימים עם הכל פתוח.',
                      'Trial — {n} days left with everything open.',
                      'Essai — encore {n} jours avec tout ouvert.',
                      'Пробный период — осталось {n} дней со всем открытым.',
                      'تجربة — بقيت {n} أيام وكل شيء مفتوح.'),
'pro.state.free':    ('התוכנית החינמית. הליבה נשארת פתוחה תמיד.',
                      'The free plan. The core always stays open.',
                      'Le plan gratuit. Le cœur reste toujours ouvert.',
                      'Бесплатный тариф. Основа всегда открыта.',
                      'الخطة المجانية. الأساس يبقى مفتوحاً دائماً.'),

# ---------- licence ----------
'pro.lic.s':      ('הקוד מגיע במייל אחרי התשלום. הוא מפעיל את פרו גם במכשיר אחר.',
                   'The key arrives by email after payment. It also opens Pro on another device.',
                   'La clé arrive par e-mail après le paiement. Elle ouvre aussi Pro sur un autre appareil.',
                   'Ключ приходит на почту после оплаты. Он открывает Pro и на другом устройстве.',
                   'يصلك المفتاح بالبريد بعد الدفع. وهو يفتح Pro على جهاز آخر أيضاً.'),
'pro.lic.ph':     ('הדבק כאן את הקוד', 'Paste the key here', 'Colle la clé ici',
                   'Вставь ключ сюда', 'الصق المفتاح هنا'),
'pro.lic.go':     ('הפעל', 'Activate', 'Activer', 'Активировать', 'تفعيل'),
'pro.lic.empty':  ('צריך להדביק קוד קודם.', 'Paste a key first.', 'Colle d\'abord une clé.',
                   'Сначала вставь ключ.', 'الصق مفتاحاً أولاً.'),
'pro.lic.checking':('בודק מול השרת…', 'Checking with the provider…', 'Vérification en cours…',
                   'Проверяем у провайдера…', 'جارٍ التحقق…'),
'pro.lic.ok':     ('פרו נפתח. תודה.', 'Pro is open. Thank you.', 'Pro est ouvert. Merci.',
                   'Pro открыт. Спасибо.', 'تم فتح Pro. شكراً لك.'),
'pro.lic.bad':    ('הקוד לא התקבל. בדוק אותו שוב, או כתוב לי.',
                   'That key was not accepted. Check it, or write to me.',
                   'Cette clé n\'a pas été acceptée. Vérifie-la, ou écris-moi.',
                   'Ключ не принят. Проверь его или напиши мне.',
                   'لم يُقبل المفتاح. تحقّق منه، أو راسلني.'),
'pro.lic.net':    ('אין חיבור כרגע. נסה שוב עוד רגע.',
                   'No connection right now. Try again in a moment.',
                   'Pas de connexion. Réessaie dans un instant.',
                   'Сейчас нет связи. Попробуй через минуту.',
                   'لا يوجد اتصال الآن. حاول بعد قليل.'),
'pro.lic.release':('שחרר את המכשיר הזה', 'Release this device', 'Libérer cet appareil',
                   'Освободить это устройство', 'حرّر هذا الجهاز'),
'pro.lic.released':('המכשיר שוחרר.', 'Device released.', 'Appareil libéré.',
                   'Устройство освобождено.', 'تم تحرير الجهاز.'),
'pro.portal':     ('לנהל את המנוי', 'Manage subscription', 'Gérer l\'abonnement',
                   'Управлять подпиской', 'إدارة الاشتراك'),

# ---------- backup ----------
'bk.t':           ('גיבוי ושחזור', 'Backup and restore', 'Sauvegarde et restauration',
                   'Резервная копия', 'نسخة احتياطية واستعادة'),
'bk.s':           ('הכל נשמר רק במכשיר הזה. קובץ גיבוי אחד הוא ההבדל בין "החלפתי טלפון" '
                   'ל"איבדתי חצי שנה". חינם, תמיד.',
                   'Everything lives on this device only. One backup file is the difference '
                   'between "I changed phones" and "I lost six months". Free, always.',
                   'Tout est stocké sur cet appareil uniquement. Un fichier de sauvegarde, c\'est la '
                   'différence entre « j\'ai changé de téléphone » et « j\'ai perdu six mois ». Gratuit, toujours.',
                   'Всё хранится только на этом устройстве. Один файл копии — это разница между '
                   '«я сменил телефон» и «я потерял полгода». Бесплатно, всегда.',
                   'كل شيء محفوظ على هذا الجهاز فقط. ملف نسخة احتياطية واحد هو الفرق بين '
                   '«غيّرت الهاتف» و«فقدت ستة أشهر». مجاناً، دائماً.'),
'bk.export':      ('שמור קובץ גיבוי', 'Save a backup', 'Enregistrer une sauvegarde',
                   'Сохранить копию', 'احفظ نسخة احتياطية'),
'bk.import':      ('שחזר מקובץ', 'Restore from a file', 'Restaurer depuis un fichier',
                   'Восстановить из файла', 'استعد من ملف'),
'bk.done':        ('הגיבוי ירד למכשיר.', 'The backup was downloaded.', 'La sauvegarde a été téléchargée.',
                   'Копия загружена.', 'تم تنزيل النسخة الاحتياطية.'),
'bk.bad':         ('זה לא קובץ גיבוי של Proactivity.', 'That is not a Proactivity backup file.',
                   'Ce n\'est pas un fichier de sauvegarde Proactivity.',
                   'Это не файл резервной копии Proactivity.',
                   'هذا ليس ملف نسخة احتياطية لـ Proactivity.'),
'bk.confirm':     ('לשחזר את הגיבוי הזה?\n\nשם: {name}\nנקודות: {pts}\nרצף: {sk}\nיעדים: {g}\n\n'
                   'כל מה שיש עכשיו במכשיר יוחלף.',
                   'Restore this backup?\n\nName: {name}\nPoints: {pts}\nStreak: {sk}\nTargets: {g}\n\n'
                   'Everything currently on this device will be replaced.',
                   'Restaurer cette sauvegarde ?\n\nNom : {name}\nPoints : {pts}\nSérie : {sk}\n'
                   'Objectifs : {g}\n\nTout ce qui est sur cet appareil sera remplacé.',
                   'Восстановить эту копию?\n\nИмя: {name}\nОчки: {pts}\nСерия: {sk}\nЦели: {g}\n\n'
                   'Всё, что сейчас на устройстве, будет заменено.',
                   'استعادة هذه النسخة؟\n\nالاسم: {name}\nالنقاط: {pts}\nالتتابع: {sk}\nالأهداف: {g}\n\n'
                   'سيُستبدل كل ما هو موجود على هذا الجهاز.'),
'bk.full':        ('האחסון במכשיר מלא. שמור גיבוי ופנה מקום.',
                   'Device storage is full. Save a backup and free some space.',
                   'Le stockage est plein. Enregistre une sauvegarde et libère de la place.',
                   'Память устройства заполнена. Сохрани копию и освободи место.',
                   'مساحة التخزين ممتلئة. احفظ نسخة احتياطية وأفرغ بعض المساحة.'),

# ---------- calendar ----------
'cal.add':        ('הוסף ליומן', 'Add to calendar', 'Ajouter au calendrier',
                   'Добавить в календарь', 'أضف إلى التقويم'),
'cal.done':       ('הקובץ ירד. פתח אותו והיומן יוסיף את זה.',
                   'The file downloaded. Open it and your calendar will add it.',
                   'Le fichier est téléchargé. Ouvre-le et ton calendrier l\'ajoutera.',
                   'Файл загружен. Открой его — календарь добавит событие.',
                   'تم تنزيل الملف. افتحه وسيضيفه التقويم.'),
'cal.time':       ('שעת התזכורת', 'Reminder time', 'Heure du rappel',
                   'Время напоминания', 'وقت التذكير'),
'cal.time.h':     ('השעה שתיכנס ליומן כשמוסיפים יעד.',
                   'The hour that goes into the calendar when you add a target.',
                   'L\'heure inscrite au calendrier quand tu ajoutes un objectif.',
                   'Час, который попадёт в календарь при добавлении цели.',
                   'الساعة التي تُسجَّل في التقويم عند إضافة هدف.'),

# ---------- install ----------
'pwa.t':          ('אפשר להתקין את זה כאפליקציה על המסך הראשי.',
                   'You can install this as an app on your home screen.',
                   'Tu peux l\'installer comme une app sur ton écran d\'accueil.',
                   'Это можно установить как приложение на домашний экран.',
                   'يمكنك تثبيت هذا كتطبيق على الشاشة الرئيسية.'),
'pwa.go':         ('התקן', 'Install', 'Installer', 'Установить', 'ثبّت'),
'pwa.no':         ('לא צריך', 'No thanks', 'Non merci', 'Не нужно', 'لا شكراً'),

# ---------- the trend ----------
'tr.sec':         ('איך זה זז', 'How it has moved', 'Comment ça a bougé',
                   'Как это менялось', 'كيف تحرّك الأمر'),
'tr.t':           ('מדד הפרואקטיביות', 'Proactivity score', 'Indice de proactivité',
                   'Индекс проактивности', 'مؤشر المبادرة'),
'tr.none':        ('אחרי שאלון שני יופיע כאן גרף שמראה מה זז ומה לא.',
                   'After a second check-in, a chart here will show what moved and what did not.',
                   'Après un deuxième bilan, un graphique montrera ici ce qui a bougé.',
                   'После второй проверки здесь появится график: что сдвинулось, а что нет.',
                   'بعد المراجعة الثانية سيظهر هنا رسم يوضّح ما تحرّك وما لم يتحرّك.'),
'tr.one':         ('יש שאלון אחד. עוד אחד בעוד חודש, ויהיה כאן קו.',
                   'One check-in so far. Another in a month and there will be a line here.',
                   'Un seul bilan pour l\'instant. Un autre dans un mois et il y aura une courbe.',
                   'Пока одна проверка. Ещё одна через месяц — и здесь будет линия.',
                   'هناك مراجعة واحدة حتى الآن. واحدة أخرى بعد شهر وسيظهر خط هنا.'),
'tr.retake':      ('לענות על השאלון שוב', 'Take the check-in again', 'Refaire le bilan',
                   'Пройти проверку заново', 'أعد المراجعة'),
'tr.since':       ('מאז {d}', 'Since {d}', 'Depuis le {d}', 'С {d}', 'منذ {d}'),
'tr.aria':        ('גרף: מדד הפרואקטיביות ב־{n} שאלונים, מ־{a} ל־{b}.',
                   'Chart: proactivity score across {n} check-ins, from {a} to {b}.',
                   'Graphique : indice de proactivité sur {n} bilans, de {a} à {b}.',
                   'График: индекс проактивности за {n} проверок, с {a} до {b}.',
                   'رسم: مؤشر المبادرة عبر {n} مراجعات، من {a} إلى {b}.'),

# ---------- goal lifecycle ----------
'gc.pause':       ('השהה', 'Pause', 'Mettre en pause', 'Пауза', 'إيقاف مؤقت'),
'gc.resume':      ('חזור אליו', 'Resume', 'Reprendre', 'Продолжить', 'استئناف'),
'gc.paused':      ('מושהה — לא נספר ברצף', 'Paused — not counted in the streak',
                   'En pause — non compté dans la série', 'На паузе — в серию не идёт',
                   'متوقف مؤقتاً — لا يُحتسب في التتابع'),
'gc.finish':      ('סיימתי את זה', 'I finished this', 'Je l\'ai terminé',
                   'Я это завершил', 'أنهيت هذا'),
'gc.done':        ('הושלם ב־{d}', 'Completed {d}', 'Terminé le {d}',
                   'Завершено {d}', 'اكتمل في {d}'),
'gc.reopen':      ('לפתוח מחדש', 'Reopen', 'Rouvrir', 'Открыть снова', 'أعد فتحه'),
't.gpaused':      ('היעד מושהה. הוא מחכה, לא נמחק.',
                   'The target is paused. It is waiting, not deleted.',
                   'L\'objectif est en pause. Il attend, il n\'est pas supprimé.',
                   'Цель на паузе. Она ждёт, а не удалена.',
                   'الهدف متوقف مؤقتاً. إنه ينتظر، لم يُحذف.'),
't.gresumed':     ('חזרנו ליעד הזה.', 'Back on this target.', 'De retour sur cet objectif.',
                   'Возвращаемся к этой цели.', 'عدنا إلى هذا الهدف.'),
't.gdone':        ('יעד הושלם. זה נשמר.', 'Target completed. It is kept.',
                   'Objectif terminé. Il est conservé.',
                   'Цель достигнута. Она сохранена.', 'اكتمل الهدف. تم حفظه.'),

# ---------- streak ----------
'd.sk.rescue':    ('פספסת יום. תעשה משהו היום והרצף של {n} נשמר.',
                   'You missed a day. Do one thing today and the {n}-day run holds.',
                   'Tu as manqué un jour. Fais une chose aujourd\'hui et la série de {n} tient.',
                   'Пропущен день. Сделай что-то сегодня — и серия из {n} сохранится.',
                   'فاتك يوم. افعل شيئاً اليوم وسيبقى تتابع الـ{n}.'),
}
