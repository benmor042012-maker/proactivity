# -*- coding: utf-8 -*-
"""The evolving avatar (XP, levels, the four ranks) and the referral programme.

Entries are 'key': (he, en, fr, ru, ar). The rank names carry a
{masculine|feminine} segment in Hebrew, Russian and Arabic, so the app calls a
woman "ההרפתקנית" and not "ההרפתקן". French keeps the four titles the brief
was written with - L'Initié, L'Aventurier, Le Conquérant, Le Titan - as fixed
names: the merged form ("Le Conquérant/La Conquérante") is too long for the
rank heading.
"""
AVATAR = {

# ---------- the avatar card ----------
'av.t':        ('הדמות שלך', 'Your avatar', 'Ton avatar', 'Твой аватар', 'شخصيتك'),
'av.s':        ('כל משימה שמושלמת מעניקה XP. בכל רף חדש הדמות גדלה, מתחזקת ומקבלת מאפיינים משלה.',
                'Every completed task earns XP. At every new threshold the avatar grows, gets stronger and gains features of its own.',
                'Chaque tâche accomplie rapporte des XP. À chaque palier, l\'avatar grandit, se renforce et gagne ses propres attributs.',
                'Каждая выполненная задача даёт XP. На каждом новом рубеже аватар растёт, крепнет и получает собственные черты.',
                'كل مهمة مكتملة تمنح XP. عند كل عتبة جديدة تكبر الشخصية وتقوى وتكتسب سمات خاصة بها.'),
'av.ladder':   ('שלבי ההתפתחות', 'The evolution ladder', 'Les paliers d\'évolution', 'Ступени развития', 'مراحل التطوّر'),
'av.lvl':      ('רמה {n}', 'Level {n}', 'Niveau {n}', 'Уровень {n}', 'المستوى {n}'),
'av.at':       ('רמה {l} · {n} XP', 'Level {l} · {n} XP', 'Niveau {l} · {n} XP', 'Уровень {l} · {n} XP', 'المستوى {l} · {n} XP'),
'av.next':     ('עוד {n} XP לרמה {l}', '{n} XP to level {l}', '{n} XP avant le niveau {l}', '{n} XP до уровня {l}', '{n} XP للمستوى {l}'),
'av.tier.next':('עוד {n} XP עד {x}', '{n} XP until {x}', '{n} XP avant {x}', '{n} XP до звания «{x}»', '{n} XP حتى {x}'),
'av.max':      ('הרף העליון. מכאן רק ממשיכים לצבור.',
                'The top tier. From here you only keep building.',
                'Le palier ultime. À partir d\'ici, on continue d\'accumuler.',
                'Высшая ступень. Дальше — только копить.',
                'أعلى مرتبة. من هنا تواصل التراكم فقط.'),
'av.lvlup':    ('רמה {n}. ממשיכים לעלות.', 'Level {n}. Keep climbing.', 'Niveau {n}. On continue de monter.',
                'Уровень {n}. Продолжаем подъём.', 'المستوى {n}. نواصل الصعود.'),
'av.rankup':   ('הדמות שלך התפתחה: {x}', 'Your avatar has evolved: {x}', 'Ton avatar a évolué : {x}',
                'Твой аватар развился: {x}', 'تطوّرت شخصيتك: {x}'),
'av.aria':     ('הדמות שלך: {x}, רמה {n}', 'Your avatar: {x}, level {n}', 'Ton avatar : {x}, niveau {n}',
                'Твой аватар: {x}, уровень {n}', 'شخصيتك: {x}، المستوى {n}'),

# ---------- the four ranks ----------
'av.r1':   ('{הטירון|הטירונית}', 'The Initiate', 'L\'Initié', '{Новичок|Новенькая}', '{المبتدئ|المبتدئة}'),
'av.r2':   ('{ההרפתקן|ההרפתקנית}', 'The Adventurer', 'L\'Aventurier', '{Искатель|Искательница}', '{المغامر|المغامرة}'),
'av.r3':   ('{הכובש|הכובשת}', 'The Conqueror', 'Le Conquérant', '{Завоеватель|Завоевательница}', '{الفاتح|الفاتحة}'),
'av.r4':   ('הטיטאן', 'The Titan', 'Le Titan', 'Титан', 'التيتان'),
'av.r1.d': ('דמות רזה, לבוש בסיסי', 'A lean figure, basic clothing', 'Silhouette fine, tenue de base',
            'Худая фигура, простая одежда', 'قوام نحيل، ملابس بسيطة'),
'av.r2.d': ('יציבה בטוחה, ציוד עור', 'A confident stance, leather gear', 'Posture assurée, équipement en cuir',
            'Уверенная стойка, кожаное снаряжение', 'وقفة واثقة، عتاد جلدي'),
'av.r3.d': ('מבנה גוף חסון, עיטורי מתכת', 'A sturdy build, metal ornaments', 'Carrure solide, ornements de métal',
            'Крепкое телосложение, металлические украшения', 'بنية قوية، زخارف معدنية'),
'av.r4.d': ('ממדי ענק, הילה זוהרת', 'Giant proportions, a glowing aura', 'Dimensions de géant, aura lumineuse',
            'Гигантские размеры, светящаяся аура', 'أبعاد عملاقة، هالة متوهجة'),

# ---------- friends bring friends ----------
'inv.t':        ('חברים מביאים חברים', 'Friends bring friends', 'Les amis amènent des amis',
                 'Друзья приводят друзей', 'الأصدقاء يجلبون الأصدقاء'),
'inv.s':        ('{שלח|שלחי} את הקישור האישי שלך למשפחה ולחברים. ברגע שחבר מסיים את ההרשמה — +{n} XP נכנסים לחשבון שלך.',
                 'Send your personal link to family and friends. The moment a friend finishes signing up, +{n} XP lands in your account.',
                 'Envoie ton lien personnel à ta famille et tes amis. Dès qu\'un ami termine son inscription, +{n} XP arrivent sur ton compte.',
                 'Отправь свою личную ссылку семье и друзьям. Как только друг завершит регистрацию, на твой счёт придёт +{n} XP.',
                 '{أرسل|أرسلي} رابطك الشخصي للعائلة والأصدقاء. بمجرد أن يُكمل صديق التسجيل — يُضاف +{n} XP إلى حسابك.'),
'inv.link':     ('הקישור שלך', 'Your link', 'Ton lien', 'Твоя ссылка', 'رابطك'),
'inv.copy':     ('העתק קישור', 'Copy link', 'Copier le lien', 'Скопировать ссылку', 'انسخ الرابط'),
'inv.share':    ('שתף', 'Share', 'Partager', 'Поделиться', 'شارك'),
'inv.copied':   ('הקישור הועתק', 'Link copied', 'Lien copié', 'Ссылка скопирована', 'تم نسخ الرابط'),
'inv.share.msg':('הצטרפו אליי ל-Proactivity — אפליקציה שהופכת כוונות לפעולות. {url}',
                 'Join me on Proactivity — the app that turns intentions into action. {url}',
                 'Rejoins-moi sur Proactivity — l\'app qui transforme les intentions en actions. {url}',
                 'Присоединяйся ко мне в Proactivity — приложение, которое превращает намерения в действия. {url}',
                 'انضموا إليّ في Proactivity — التطبيق الذي يحوّل النوايا إلى أفعال. {url}'),
'inv.how.t':    ('איך זה עובד?', 'How does it work?', 'Comment ça marche ?', 'Как это работает?', 'كيف يعمل؟'),
'inv.how':      ('החבר נכנס דרך הקישור ומסיים את ההרשמה. בסיום מופיע אצלו קוד אישור קצר, והוא שולח לך אותו. '
                 '{הדבק|הדביקי} אותו כאן — וה-XP נזקף מיד. הכל נשאר במכשיר, בלי שרת ובלי חשבון.',
                 'Your friend opens the link and finishes signing up. At the end they see a short confirmation code and send it to you. '
                 'Paste it here — and the XP is credited immediately. Everything stays on the device, with no server and no account.',
                 'Ton ami ouvre le lien et termine son inscription. À la fin, un court code de confirmation s\'affiche chez lui, qu\'il t\'envoie. '
                 'Colle-le ici — et les XP sont crédités aussitôt. Tout reste sur l\'appareil, sans serveur ni compte.',
                 'Друг открывает ссылку и завершает регистрацию. В конце у него появляется короткий код подтверждения, который он отправляет тебе. '
                 'Вставь его сюда — и XP начисляются сразу. Всё остаётся на устройстве, без сервера и без аккаунта.',
                 'يفتح صديقك الرابط ويُكمل التسجيل. في النهاية يظهر لديه رمز تأكيد قصير يرسله إليك. '
                 '{الصقه|الصقيه} هنا — ويُضاف XP فوراً. كل شيء يبقى على الجهاز، بلا خادم وبلا حساب.'),
'inv.code.ph':  ('קוד אישור מחבר', 'Confirmation code from a friend', 'Code de confirmation d\'un ami',
                 'Код подтверждения от друга', 'رمز تأكيد من صديق'),
'inv.redeem':   ('הפעל', 'Redeem', 'Valider', 'Активировать', 'تفعيل'),
'inv.ok':       ('+{n} XP. חבר הצטרף בזכותך.', '+{n} XP. A friend joined because of you.',
                 '+{n} XP. Un ami a rejoint grâce à toi.', '+{n} XP. Друг присоединился благодаря тебе.',
                 '+{n} XP. انضم صديق بفضلك.'),
'inv.bad':      ('הקוד לא תואם את הקישור שלך. {בדוק|בדקי} שהחבר נרשם דרכו.',
                 'That code does not match your link. Check that your friend signed up through it.',
                 'Ce code ne correspond pas à ton lien. Vérifie que ton ami s\'est inscrit via ce lien.',
                 'Этот код не соответствует твоей ссылке. Проверь, что друг зарегистрировался по ней.',
                 'الرمز لا يطابق رابطك. {تأكّد|تأكّدي} أن صديقك سجّل عبره.'),
'inv.dup':      ('הקוד הזה כבר הופעל.', 'This code was already redeemed.', 'Ce code a déjà été utilisé.',
                 'Этот код уже активирован.', 'هذا الرمز مُفعّل من قبل.'),
'inv.self':     ('זה הקוד שלך. הוא מיועד לחברים.', 'That is your own code. It is for friends.',
                 'C\'est ton propre code. Il est destiné à tes amis.', 'Это твой собственный код. Он для друзей.',
                 'هذا رمزك أنت. إنه مخصّص للأصدقاء.'),
'inv.count':    ('{n} חברים הצטרפו דרכך', '{n} friends joined through you', '{n} amis ont rejoint grâce à toi',
                 'Через тебя присоединились: {n}', 'انضم {n} من الأصدقاء عبرك'),
'inv.from.t':   ('הצטרפת דרך הזמנה', 'You joined through an invite', 'Tu as rejoint via une invitation',
                 'Ты пришёл{|ла} по приглашению', 'انضممت عبر دعوة'),
'inv.from.s':   ('מי שהזמין אותך מקבל +{n} XP ברגע שהקוד הזה מגיע אליו. {שלח|שלחי} לו אותו.',
                 'Whoever invited you gets +{n} XP the moment this code reaches them. Send it to them.',
                 'La personne qui t\'a invité reçoit +{n} XP dès que ce code lui parvient. Envoie-le-lui.',
                 'Тот, кто тебя пригласил, получит +{n} XP, как только этот код дойдёт до него. Отправь ему код.',
                 'من دعاك يحصل على +{n} XP بمجرد وصول هذا الرمز إليه. {أرسله|أرسليه} له.'),
'inv.from.send':('שלח את הקוד', 'Send the code', 'Envoyer le code', 'Отправить код', 'أرسل الرمز'),
'inv.from.done':('נשלח', 'Sent', 'Envoyé', 'Отправлено', 'تم الإرسال'),
'inv.msg':      ('הצטרפתי ל-Proactivity דרך ההזמנה שלך. קוד האישור: {c}',
                 'I joined Proactivity through your invite. Confirmation code: {c}',
                 'J\'ai rejoint Proactivity via ton invitation. Code de confirmation : {c}',
                 'Я присоединился к Proactivity по твоему приглашению. Код подтверждения: {c}',
                 'انضممت إلى Proactivity عبر دعوتك. رمز التأكيد: {c}'),
'inv.code.copied':('הקוד הועתק', 'Code copied', 'Code copié', 'Код скопирован', 'تم نسخ الرمز'),
}
