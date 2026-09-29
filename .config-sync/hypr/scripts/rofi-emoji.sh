#!/bin/bash

selection=$(
    sed '1,/^### DATA ###$/d' "$0" \
    | rofi -dmenu -i -config ~/.config/rofi/themes/rofi-emoji.rasi \
    | cut -d ' ' -f 1 \
    | tr -d '\n'
)

[ -z "$selection" ] && exit 0

printf "%s" "$selection" | wl-copy

# Type the emoji into the currently focused pane/window after rofi closes.
if command -v wtype >/dev/null 2>&1; then
    sleep 0.1
    wtype -- "$selection"
elif command -v ydotool >/dev/null 2>&1; then
    sleep 0.1
    echo -n "$selection" | ydotool type -
fi

exit 0

### DATA ###
😀 grinning face face smile happy joy :D grin
😃 grinning face with big eyes face happy joy haha :D :) smile funny
😄 grinning face with smiling eyes face happy joy funny haha laugh like :D :) smile
😁 beaming face with smiling eyes face happy smile joy kawaii
😆 grinning squinting face happy joy lol satisfied haha face glad XD laugh
😅 grinning face with sweat face hot happy laugh sweat smile relief
🤣 rolling on the floor laughing face rolling floor laughing lol haha rofl
😂 face with tears of joy face cry tears weep happy happytears haha
🙂 slightly smiling face face smile
🙃 upside down face face flipped silly smile
😉 winking face face happy mischievous secret ;) smile eye
😊 smiling face with smiling eyes face smile happy flushed crush embarrassed shy joy
😇 smiling face with halo face angel heaven halo
🥰 smiling face with hearts face love like affection valentines infatuation crush hearts adore
😍 smiling face with heart eyes face love like affection valentines infatuation crush heart
🤩 star struck face smile starry eyes grinning
😘 face blowing a kiss face love like affection valentines infatuation kiss
😗 kissing face love like face 3 valentines infatuation kiss
☺️  smiling face face blush massage happiness
😚 kissing face with closed eyes face love like affection valentines infatuation kiss
😙 kissing face with smiling eyes face affection valentines infatuation kiss
😋 face savoring food happy joy tongue smile face silly yummy nom delicious savouring
😛 face with tongue face prank childish playful mischievous smile tongue
😜 winking face with tongue face prank childish playful mischievous smile wink tongue
🤪 zany face face goofy crazy
😝 squinting face with tongue face prank playful mischievous smile tongue
🤑 money mouth face face rich dollar money
🤗 hugging face face smile hug
🤭 face with hand over mouth face whoops shock surprise
🤫 shushing face face quiet shhh
🤔 thinking face face hmmm think consider
🤐 zipper mouth face face sealed zipper secret
🤨 face with raised eyebrow face distrust scepticism disapproval disbelief surprise
😐 neutral face indifference meh :| neutral
😑 expressionless face face indifferent - - meh deadpan
😶 face without mouth face hellokitty
😏 smirking face face smile mean prank smug sarcasm
😒 unamused face indifference bored straight face serious sarcasm unimpressed skeptical dubious side eye
🙄 face with rolling eyes face eyeroll frustrated
😬 grimacing face face grimace teeth
🤥 lying face face lie pinocchio
😌 relieved face face relaxed phew massage happiness
😔 pensive face face sad depressed upset
😪 sleepy face face tired rest nap
🤤 drooling face face
😴 sleeping face face tired sleepy night zzz
😷 face with medical mask face sick ill disease
🤒 face with thermometer sick temperature thermometer cold fever
🤕 face with head bandage injured clumsy bandage hurt
🤢 nauseated face face vomit gross green sick throw up ill
🤮 face vomiting face sick
🤧 sneezing face face gesundheit sneeze sick allergy
🥵 hot face face feverish heat red sweating
🥶 cold face face blue freezing frozen frostbite icicles
🥴 woozy face face dizzy intoxicated tipsy wavy
😵 dizzy face spent unconscious xox dizzy
🤯 exploding head face shocked mind blown
🤠 cowboy hat face face cowgirl hat
🥳 partying face face celebration woohoo
😎 smiling face with sunglasses face cool smile summer beach sunglass
🤓 nerd face face nerdy geek dork
🧐 face with monocle face stuffy wealthy
😕 confused face face indifference huh weird hmmm :/
😟 worried face face concern nervous :(
🙁 slightly frowning face face frowning disappointed sad upset
☹️  frowning face face sad upset frown
😮 face with open mouth face surprise impressed wow whoa :O
😯 hushed face face woo shh
😲 astonished face face xox surprised poisoned
😳 flushed face face blush shy flattered
🥺 pleading face face begging mercy
😦 frowning face with open mouth face aw what
😧 anguished face face stunned nervous
😨 fearful face face scared terrified nervous oops huh
😰 anxious face with sweat face nervous sweat
😥 sad but relieved face face phew sweat nervous
😢 crying face face tears sad depressed upset :'(
😭 loudly crying face face cry tears sad upset depressed
😱 face screaming in fear face munch scared omg
😖 confounded face face confused sick unwell oops :S
😣 persevering face face sick no upset oops
😞 disappointed face face sad upset depressed :(
😓 downcast face with sweat face hot sad tired exercise
😩 weary face face tired sleepy sad frustrated upset
😫 tired face sick whine upset frustrated
🥱 yawning face tired sleepy
😤 face with steam from nose face gas phew proud pride
😡 pouting face angry mad hate despise
😠 angry face mad face annoyed frustrated
🤬 face with symbols on mouth face swearing cursing cussing profanity expletive
😈 smiling face with horns devil horns
👿 angry face with horns devil angry horns
💀 skull dead skeleton creepy death
☠️ skull and crossbones poison danger deadly scary death pirate evil
💩 pile of poo hankey shitface fail turd shit
🤡 clown face face
👹 ogre monster red mask halloween scary creepy devil demon japanese ogre
👺 goblin red evil mask monster scary creepy japanese goblin
👻 ghost halloween spooky scary
👽 alien UFO paul weird outer space
👾 alien monster game arcade play
🤖 robot computer machine bot
😺 grinning cat animal cats happy smile
😸 grinning cat with smiling eyes animal cats smile
😹 cat with tears of joy animal cats haha happy tears
😻 smiling cat with heart eyes animal love like affection cats valentines heart
😼 cat with wry smile animal cats smirk
😽 kissing cat animal cats kiss
🙀 weary cat animal cats munch scared scream
😿 crying cat animal tears weep sad cats upset cry
😾 pouting cat animal cats
🙈 see no evil monkey monkey animal nature haha
🙉 hear no evil monkey animal monkey nature
🙊 speak no evil monkey monkey animal nature omg
💋 kiss mark face lips love like affection valentines
💌 love letter email like affection envelope valentines
💘 heart with arrow love like heart affection valentines
💝 heart with ribbon love valentines
💖 sparkling heart love like affection valentines
💗 growing heart like love affection valentines pink
💓 beating heart love like affection valentines pink heart
💞 revolving hearts love like affection valentines
💕 two hearts love like affection valentines heart
💟 heart decoration purple-square love like
❣️  heart exclamation decoration love
💔 broken heart sad sorry break heart heartbreak
❤️  red heart love like valentines
🧡 orange heart love like affection valentines
💛 yellow heart love like affection valentines
💚 green heart love like affection valentines
💙 blue heart love like affection valentines
💜 purple heart love like affection valentines
🤎 brown heart coffee
🖤 black heart evil
🤍 white heart pure
💯 hundred points score perfect numbers century exam quiz test pass hundred
💢 anger symbol angry mad
💥 collision bomb explode explosion collision blown
💫 dizzy star sparkle shoot magic
💦 sweat droplets water drip oops
💨 dashing away wind air fast shoo fart smoke puff
🕳️ hole embarrassing
💣 bomb boom explode explosion terrorism
💬 speech balloon bubble words message talk chatting
👁️‍🗨️ eye in speech bubble info
🗨️ left speech bubble words message talk chatting
🗯️ right anger bubble caption speech thinking mad
💭 thought balloon bubble cloud speech thinking dream
💤 zzz sleepy tired dream
👋 waving hand hands gesture goodbye solong farewell hello hi palm
🤚 raised back of hand fingers raised backhand
🖐️ hand with fingers splayed hand fingers palm
✋ raised hand fingers stop highfive palm ban
🖖 vulcan salute hand fingers spock star trek
👌 ok hand fingers limbs perfect ok okay
🤏 pinching hand tiny small size
✌️ victory hand fingers ohyeah hand peace victory two
🤞 crossed fingers good lucky
🤟 love you gesture hand fingers gesture
🤘 sign of the horns hand fingers evil eye sign of horns rock on
🤙 call me hand hands gesture shaka
👈 backhand index pointing left direction fingers hand left
👉 backhand index pointing right fingers hand direction right
👆 backhand index pointing up fingers hand direction up
🖕 middle finger hand fingers rude middle flipping
👇 backhand index pointing down fingers hand direction down
☝️  index pointing up hand fingers direction up
👍 thumbs up thumbsup yes awesome good agree accept cool hand like +1
👎 thumbs down thumbsdown no dislike hand -1
✊ raised fist fingers hand grasp
👊 oncoming fist angry violence fist hit attack hand
🤛 left facing fist hand fistbump
🤜 right facing fist hand fistbump
👏 clapping hands hands praise applause congrats yay
🙌 raising hands gesture hooray yea celebration hands
👐 open hands fingers butterfly hands open
🤲 palms up together hands gesture cupped prayer
🤝 handshake agreement shake
🙏 folded hands please hope wish namaste highfive pray
✍️  writing hand lower left ballpoint pen stationery write compose
💅 nail polish beauty manicure finger fashion nail
🤳 selfie camera phone
💪 flexed biceps arm flex hand summer strong biceps
🦾 mechanical arm accessibility
🦿 mechanical leg accessibility
🦵 leg kick limb
🦶 foot kick stomp
👂 ear face hear sound listen
🦻 ear with hearing aid accessibility
👃 nose smell sniff
🧠 brain smart intelligent
🦷 tooth teeth dentist
🦴 bone skeleton
👀 eyes look watch stalk peek see
👁️ eye face look see watch stare
👅 tongue mouth playful
👄 mouth mouth kiss
👶 baby child boy girl toddler
🧒 child gender-neutral young
👦 boy man male guy teenager
👧 girl female woman teenager
🧑 person gender-neutral person
👱 person blond hair hairstyle
👨 man mustache father dad guy classy sir moustache
🧔 man beard person bewhiskered
👨‍🦰 man red hair hairstyle
👨‍🦱 man curly hair hairstyle
👨‍🦳 man white hair old elder
👨‍🦲 man bald hairless
👩 woman female girls lady
👩‍🦰 woman red hair hairstyle
🧑‍🦰 person red hair hairstyle
👩‍🦱 woman curly hair hairstyle
🧑‍🦱 person curly hair hairstyle
👩‍🦳 woman white hair old elder
🧑‍🦳 person white hair elder old
👩‍🦲 woman bald hairless
🧑‍🦲 person bald hairless
👱‍♀️ woman blond hair woman female girl blonde person
👱‍♂️ man blond hair man male boy blonde guy person
🧓 older person human elder senior gender-neutral
👴 old man human male men old elder senior
👵 old woman human female women lady old elder senior
🙍 person frowning worried
🙍‍♂️ man frowning male boy man sad depressed discouraged unhappy
🙍‍♀️ woman frowning female girl woman sad depressed discouraged unhappy
🙎 person pouting upset
🙎‍♂️ man pouting male boy man
🙎‍♀️ woman pouting female girl woman
🙅 person gesturing no decline
🙅‍♂️ man gesturing no male boy man nope
🙅‍♀️ woman gesturing no female girl woman nope
🙆 person gesturing ok agree
🙆‍♂️ man gesturing ok men boy male blue human man
🙆‍♀️ woman gesturing ok women girl female pink human woman
💁 person tipping hand information
💁‍♂️ man tipping hand male boy man human information
💁‍♀️ woman tipping hand female girl woman human information
🙋 person raising hand question
🙋‍♂️ man raising hand male boy man
🙋‍♀️ woman raising hand female girl woman
🧏 deaf person accessibility
🧏‍♂️ deaf man accessibility
🧏‍♀️ deaf woman accessibility
🙇 person bowing respectiful
🙇‍♂️ man bowing man male boy
🙇‍♀️ woman bowing woman female girl
🤦 person facepalming disappointed
🤦‍♂️ man facepalming man male boy disbelief
🤦‍♀️ woman facepalming woman female girl disbelief
🤷 person shrugging regardless
🤷‍♂️ man shrugging man male boy confused indifferent doubt
🤷‍♀️ woman shrugging woman female girl confused indifferent doubt
🧑‍⚕️ health worker hospital
👨‍⚕️ man health worker doctor nurse therapist healthcare man human
👩‍⚕️ woman health worker doctor nurse therapist healthcare woman human
🧑‍🎓 student learn
👨‍🎓 man student graduate man human
👩‍🎓 woman student graduate woman human
🧑‍🏫 teacher professor
👨‍🏫 man teacher instructor professor man human
👩‍🏫 woman teacher instructor professor woman human
🧑‍⚖️ judge law
👨‍⚖️ man judge justice court man human
👩‍⚖️ woman judge justice court woman human
🧑‍🌾 farmer crops
👨‍🌾 man farmer rancher gardener man human
👩‍🌾 woman farmer rancher gardener woman human
🧑‍🍳 cook food kitchen culinary
👨‍🍳 man cook chef man human
👩‍🍳 woman cook chef woman human
🧑‍🔧 mechanic worker technician
👨‍🔧 man mechanic plumber man human wrench
👩‍🔧 woman mechanic plumber woman human wrench
🧑‍🏭 factory worker labor
👨‍🏭 man factory worker assembly industrial man human
👩‍🏭 woman factory worker assembly industrial woman human
🧑‍💼 office worker business
👨‍💼 man office worker business manager man human
👩‍💼 woman office worker business manager woman human
🧑‍🔬 scientist chemistry
👨‍🔬 man scientist biologist chemist engineer physicist man human
👩‍🔬 woman scientist biologist chemist engineer physicist woman human
🧑‍💻 technologist computer
👨‍💻 man technologist coder developer engineer programmer software man human laptop computer
👩‍💻 woman technologist coder developer engineer programmer software woman human laptop computer
🧑‍🎤 singer song artist performer
👨‍🎤 man singer rockstar entertainer man human
👩‍🎤 woman singer rockstar entertainer woman human
🧑‍🎨 artist painting draw creativity
👨‍🎨 man artist painter man human
👩‍🎨 woman artist painter woman human
🧑‍✈️ pilot fly plane airplane
👨‍✈️ man pilot aviator plane man human
👩‍✈️ woman pilot aviator plane woman human
🧑‍🚀 astronaut outerspace
👨‍🚀 man astronaut space rocket man human
👩‍🚀 woman astronaut space rocket woman human
🧑‍🚒 firefighter fire
👨‍🚒 man firefighter fireman man human
👩‍🚒 woman firefighter fireman woman human
👮 police officer cop
👮‍♂️ man police officer man police law legal enforcement arrest 911
👮‍♀️ woman police officer woman police law legal enforcement arrest 911 female
🕵️ detective human spy detective
🕵️‍♂️ man detective crime
🕵️‍♀️ woman detective human spy detective female woman
💂 guard protect
💂‍♂️ man guard uk gb british male guy royal
💂‍♀️ woman guard uk gb british female royal woman
👷 construction worker labor build
👷‍♂️ man construction worker male human wip guy build construction worker labor
👷‍♀️ woman construction worker female human wip build construction worker labor woman
🤴 prince boy man male crown royal king
👸 princess girl woman female blond crown royal queen
👳 person wearing turban headdress
👳‍♂️ man wearing turban male indian hinduism arabs
👳‍♀️ woman wearing turban female indian hinduism arabs woman
👲 man with skullcap male boy chinese
🧕 woman with headscarf female hijab mantilla tichel
🤵 man in tuxedo couple marriage wedding groom
👰 bride with veil couple marriage wedding woman bride
🤰 pregnant woman baby
🤱 breast feeding nursing baby
👼 baby angel heaven wings halo
🎅 santa claus festival man male xmas father christmas
🤶 mrs claus woman female xmas mother christmas
🦸 superhero marvel
🦸‍♂️ man superhero man male good hero superpowers
🦸‍♀️ woman superhero woman female good heroine superpowers
🦹 supervillain marvel
🦹‍♂️ man supervillain man male evil bad criminal hero superpowers
🦹‍♀️ woman supervillain woman female evil bad criminal heroine superpowers
🧙 mage magic
🧙‍♂️ man mage man male mage sorcerer
🧙‍♀️ woman mage woman female mage witch
🧚 fairy wings magical
🧚‍♂️ man fairy man male
🧚‍♀️ woman fairy woman female
🧛 vampire blood twilight
🧛‍♂️ man vampire man male dracula
🧛‍♀️ woman vampire woman female
🧜 merperson sea
🧜‍♂️ merman man male triton
🧜‍♀️ mermaid woman female merwoman ariel
🧝 elf magical
🧝‍♂️ man elf man male
🧝‍♀️ woman elf woman female
🧞 genie magical wishes
🧞‍♂️ man genie man male
🧞‍♀️ woman genie woman female
🧟 zombie dead
🧟‍♂️ man zombie man male dracula undead walking dead
🧟‍♀️ woman zombie woman female undead walking dead
💆 person getting massage relax
💆‍♂️ man getting massage male boy man head
💆‍♀️ woman getting massage female girl woman head
💇 person getting haircut hairstyle
💇‍♂️ man getting haircut male boy man
💇‍♀️ woman getting haircut female girl woman
🚶 person walking move
🚶‍♂️ man walking human feet steps
🚶‍♀️ woman walking human feet steps woman female
🧍 person standing still
🧍‍♂️ man standing still
🧍‍♀️ woman standing still
🧎 person kneeling pray respectful
🧎‍♂️ man kneeling pray respectful
🧎‍♀️ woman kneeling respectful pray
🧑‍🦯 person with probing cane blind
👨‍🦯 man with probing cane blind
👩‍🦯 woman with probing cane blind
🧑‍🦼 person in motorized wheelchair disability accessibility
👨‍🦼 man in motorized wheelchair disability accessibility
👩‍🦼 woman in motorized wheelchair disability accessibility
🧑‍🦽 person in manual wheelchair disability accessibility
👨‍🦽 man in manual wheelchair disability accessibility
👩‍🦽 woman in manual wheelchair disability accessibility
🏃 person running move
🏃‍♂️ man running man walking exercise race running
🏃‍♀️ woman running woman walking exercise race running female
💃 woman dancing female girl woman fun
🕺 man dancing male boy fun dancer
🕴️ man in suit levitating suit business levitate hover jump
👯 people with bunny ears perform costume
👯‍♂️ men with bunny ears male bunny men boys
👯‍♀️ women with bunny ears female bunny women girls
🧖 person in steamy room relax spa
🧖‍♂️ man in steamy room male man spa steamroom sauna
🧖‍♀️ woman in steamy room female woman spa steamroom sauna
🧗 person climbing sport
🧗‍♂️ man climbing sports hobby man male rock
🧗‍♀️ woman climbing sports hobby woman female rock
🤺 person fencing sports fencing sword
🏇 horse racing animal betting competition gambling luck
⛷️ skier sports winter snow
🏂 snowboarder sports winter
🏌️ person golfing sports business
🏌️‍♂️ man golfing sport
🏌️‍♀️ woman golfing sports business woman female
🏄 person surfing sport sea
🏄‍♂️ man surfing sports ocean sea summer beach
🏄‍♀️ woman surfing sports ocean sea summer beach woman female
🚣 person rowing boat sport move
🚣‍♂️ man rowing boat sports hobby water ship
🚣‍♀️ woman rowing boat sports hobby water ship woman female
🏊 person swimming sport pool
🏊‍♂️ man swimming sports exercise human athlete water summer
🏊‍♀️ woman swimming sports exercise human athlete water summer woman female
⛹️ person bouncing ball sports human
⛹️‍♂️ man bouncing ball sport
⛹️‍♀️ woman bouncing ball sports human woman female
🏋️ person lifting weights sports training exercise
🏋️‍♂️ man lifting weights sport
🏋️‍♀️ woman lifting weights sports training exercise woman female
🚴 person biking sport move
🚴‍♂️ man biking sports bike exercise hipster
🚴‍♀️ woman biking sports bike exercise hipster woman female
🚵 person mountain biking sport move
🚵‍♂️ man mountain biking transportation sports human race bike
🚵‍♀️ woman mountain biking transportation sports human race bike woman female
🤸 person cartwheeling sport gymnastic
🤸‍♂️ man cartwheeling gymnastics
🤸‍♀️ woman cartwheeling gymnastics
🤼 people wrestling sport
🤼‍♂️ men wrestling sports wrestlers
🤼‍♀️ women wrestling sports wrestlers
🤽 person playing water polo sport
🤽‍♂️ man playing water polo sports pool
🤽‍♀️ woman playing water polo sports pool
🤾 person playing handball sport
🤾‍♂️ man playing handball sports
🤾‍♀️ woman playing handball sports
🤹 person juggling performance balance
🤹‍♂️ man juggling juggle balance skill multitask
🤹‍♀️ woman juggling juggle balance skill multitask
🧘 person in lotus position meditate
🧘‍♂️ man in lotus position man male meditation yoga serenity zen mindfulness
🧘‍♀️ woman in lotus position woman female meditation yoga serenity zen mindfulness
🛀 person taking bath clean shower bathroom
🛌 person in bed bed rest
🧑‍🤝‍🧑 people holding hands friendship
👭 women holding hands pair friendship couple love like female people human
👫 woman and man holding hands pair people human love date dating like affection valentines marriage
👬 men holding hands pair couple love like bromance friendship people human
💏 kiss pair valentines love like dating marriage
👩‍❤️‍💋‍👨 kiss woman man love
👨‍❤️‍💋‍👨 kiss man man pair valentines love like dating marriage
👩‍❤️‍💋‍👩 kiss woman woman pair valentines love like dating marriage
💑 couple with heart pair love like affection human dating valentines marriage
👩‍❤️‍👨 couple with heart woman man love
👨‍❤️‍👨 couple with heart man man pair love like affection human dating valentines marriage
👩‍❤️‍👩 couple with heart woman woman pair love like affection human dating valentines marriage
👪 family home parents child mom dad father mother people human
👨‍👩‍👦 family man woman boy love
👨‍👩‍👧 family man woman girl home parents people human child
👨‍👩‍👧‍👦 family man woman girl boy home parents people human children
👨‍👩‍👦‍👦 family man woman boy boy home parents people human children
👨‍👩‍👧‍👧 family man woman girl girl home parents people human children
👨‍👨‍👦 family man man boy home parents people human children
👨‍👨‍👧 family man man girl home parents people human children
👨‍👨‍👧‍👦 family man man girl boy home parents people human children
👨‍👨‍👦‍👦 family man man boy boy home parents people human children
👨‍👨‍👧‍👧 family man man girl girl home parents people human children
👩‍👩‍👦 family woman woman boy home parents people human children
👩‍👩‍👧 family woman woman girl home parents people human children
👩‍👩‍👧‍👦 family woman woman girl boy home parents people human children
👩‍👩‍👦‍👦 family woman woman boy boy home parents people human children
👩‍👩‍👧‍👧 family woman woman girl girl home parents people human children
👨‍👦 family man boy home parent people human child
👨‍👦‍👦 family man boy boy home parent people human children
👨‍👧 family man girl home parent people human child
👨‍👧‍👦 family man girl boy home parent people human children
👨‍👧‍👧 family man girl girl home parent people human children
👩‍👦 family woman boy home parent people human child
👩‍👦‍👦 family woman boy boy home parent people human children
👩‍👧 family woman girl home parent people human child
👩‍👧‍👦 family woman girl boy home parent people human children
👩‍👧‍👧 family woman girl girl home parent people human children
🗣️ speaking head user person human sing say talk
👤 bust in silhouette user person human
👥 busts in silhouette user person human group team
👣 footprints feet tracking walking beach
🐵 monkey face animal nature circus
🐒 monkey animal nature banana circus
🦍 gorilla animal nature circus
🦧 orangutan animal
🐶 dog face animal friend nature woof puppy pet faithful
🐕 dog animal nature friend doge pet faithful
🦮 guide dog animal blind
🐕‍🦺 service dog blind animal
🐩 poodle dog animal 101 nature pet
🐺 wolf animal nature wild
🦊 fox animal nature face
🦝 raccoon animal nature
🐱 cat face animal meow nature pet kitten
🐈 cat animal meow pet cats
🦁 lion animal nature
🐯 tiger face animal cat danger wild nature roar
🐅 tiger animal nature roar
🐆 leopard animal nature
🐴 horse face animal brown nature
🐎 horse animal gamble luck
🦄 unicorn animal nature mystical
🦓 zebra animal nature stripes safari
🦌 deer animal nature horns venison
🐮 cow face beef ox animal nature moo milk
🐂 ox animal cow beef
🐃 water buffalo animal nature ox cow
🐄 cow beef ox animal nature moo milk
🐷 pig face animal oink nature
🐖 pig animal nature
🐗 boar animal nature
🐽 pig nose animal oink
🐏 ram animal sheep nature
🐑 ewe animal nature wool shipit
🐐 goat animal nature
🐪 camel animal hot desert hump
🐫 two hump camel animal nature hot desert hump
🦙 llama animal nature alpaca
🦒 giraffe animal nature spots safari
🐘 elephant animal nature nose th circus
🦏 rhinoceros animal nature horn
🦛 hippopotamus animal nature
🐭 mouse face animal nature cheese wedge rodent
🐁 mouse animal nature rodent
🐀 rat animal mouse rodent
🐹 hamster animal nature
🐰 rabbit face animal nature pet spring magic bunny
🐇 rabbit animal nature pet magic spring
🐿️ chipmunk animal nature rodent squirrel
🦔 hedgehog animal nature spiny
🦇 bat animal nature blind vampire
🐻 bear animal nature wild
🐨 koala animal nature
🐼 panda animal nature panda
🦥 sloth animal
🦦 otter animal
🦨 skunk animal
🦘 kangaroo animal nature australia joey hop marsupial
🦡 badger animal nature honey
🐾 paw prints animal tracking footprints dog cat pet feet
🦃 turkey animal bird
🐔 chicken animal cluck nature bird
🐓 rooster animal nature chicken
🐣 hatching chick animal chicken egg born baby bird
🐤 baby chick animal chicken bird
🐥 front facing baby chick animal chicken baby bird
🐦 bird animal nature fly tweet spring
🐧 penguin animal nature
🕊️ dove animal bird
🦅 eagle animal nature bird
🦆 duck animal nature bird mallard
🦢 swan animal nature bird
🦉 owl animal nature bird hoot
🦩 flamingo animal
🦚 peacock animal nature peahen bird
🦜 parrot animal nature bird pirate talk
🐸 frog animal nature croak toad
🐊 crocodile animal nature reptile lizard alligator
🐢 turtle animal slow nature tortoise
🦎 lizard animal nature reptile
🐍 snake animal evil nature hiss python
🐲 dragon face animal myth nature chinese green
🐉 dragon animal myth nature chinese green
🦕 sauropod animal nature dinosaur brachiosaurus brontosaurus diplodocus extinct
🦖 t rex animal nature dinosaur tyrannosaurus extinct
🐳 spouting whale animal nature sea ocean
🐋 whale animal nature sea ocean
🐬 dolphin animal nature fish sea ocean flipper fins beach
🐟 fish animal food nature
🐠 tropical fish animal swim ocean beach nemo
🐡 blowfish animal nature food sea ocean
🦈 shark animal nature fish sea ocean jaws fins beach
🐙 octopus animal creature ocean sea nature beach
🐚 spiral shell nature sea beach
🐌 snail slow animal shell
🦋 butterfly animal insect nature caterpillar
🐛 bug animal insect nature worm
🐜 ant animal insect nature bug
🐝 honeybee animal insect nature bug spring honey
🐞 lady beetle animal insect nature ladybug
🦗 cricket animal cricket chirp
🕷️ spider animal arachnid
🕸️ spider web animal insect arachnid silk
🦂 scorpion animal arachnid
🦟 mosquito animal nature insect malaria
🦠 microbe amoeba bacteria germs virus
💐 bouquet flowers nature spring
🌸 cherry blossom nature plant spring flower
💮 white flower japanese spring
🏵️ rosette flower decoration military
🌹 rose flowers valentines love spring
🥀 wilted flower plant nature flower
🌺 hibiscus plant vegetable flowers beach
🌻 sunflower nature plant fall
🌼 blossom nature flowers yellow
🌷 tulip flowers plant nature summer spring
🌱 seedling plant nature grass lawn spring
🌲 evergreen tree plant nature
🌳 deciduous tree plant nature
🌴 palm tree plant vegetable nature summer beach mojito tropical
🌵 cactus vegetable plant nature
🌾 sheaf of rice nature plant
🌿 herb vegetable plant medicine weed grass lawn
☘️ shamrock vegetable plant nature irish clover
🍀 four leaf clover vegetable plant nature lucky irish
🍁 maple leaf nature plant vegetable ca fall
🍂 fallen leaf nature plant vegetable leaves
🍃 leaf fluttering in wind nature plant tree vegetable grass lawn spring
🍇 grapes fruit food wine
🍈 melon fruit nature food
🍉 watermelon fruit food picnic summer
🍊 tangerine food fruit nature orange
🍋 lemon fruit nature
🍌 banana fruit food monkey
🍍 pineapple fruit nature food
🥭 mango fruit food tropical
🍎 red apple fruit mac school
🍏 green apple fruit nature
🍐 pear fruit nature food
🍑 peach fruit nature food
🍒 cherries food fruit
🍓 strawberry fruit food nature
🥝 kiwi fruit fruit food
🍅 tomato fruit vegetable nature food
🥥 coconut fruit nature food palm
🥑 avocado fruit food
🍆 eggplant vegetable nature food aubergine
🥔 potato food tuber vegatable starch
🥕 carrot vegetable food orange
🌽 ear of corn food vegetable plant
🌶️ hot pepper food spicy chilli chili
🥒 cucumber fruit food pickle
🥬 leafy green food vegetable plant bok choy cabbage kale lettuce
🥦 broccoli fruit food vegetable
🧄 garlic food spice cook
🧅 onion cook food spice
🍄 mushroom plant vegetable
🥜 peanuts food nut
🌰 chestnut food squirrel
🍞 bread food wheat breakfast toast
🥐 croissant food bread french
🥖 baguette bread food bread french
🥨 pretzel food bread twisted
🥯 bagel food bread bakery schmear
🥞 pancakes food breakfast flapjacks hotcakes
🧇 waffle food breakfast
🧀 cheese wedge food chadder
🍖 meat on bone good food drumstick
🍗 poultry leg food meat drumstick bird chicken turkey
🥩 cut of meat food cow meat cut chop lambchop porkchop
🥓 bacon food breakfast pork pig meat
🍔 hamburger meat fast food beef cheeseburger mcdonalds burger king
🍟 french fries chips snack fast food
🍕 pizza food party
🌭 hot dog food frankfurter
🥪 sandwich food lunch bread
🌮 taco food mexican
🌯 burrito food mexican
🥙 stuffed flatbread food flatbread stuffed gyro
🧆 falafel food
🥚 egg food chicken breakfast
🍳 cooking food breakfast kitchen egg
🥘 shallow pan of food food cooking casserole paella
🍲 pot of food food meat soup
🥣 bowl with spoon food breakfast cereal oatmeal porridge
🥗 green salad food healthy lettuce
🍿 popcorn food movie theater films snack
🧈 butter food cook
🧂 salt condiment shaker
🥫 canned food food soup
🍱 bento box food japanese box
🍘 rice cracker food japanese
🍙 rice ball food japanese
🍚 cooked rice food china asian
🍛 curry rice food spicy hot indian
🍜 steaming bowl food japanese noodle chopsticks
🍝 spaghetti food italian noodle
🍠 roasted sweet potato food nature
🍢 oden food japanese
🍣 sushi food fish japanese rice
🍤 fried shrimp food animal appetizer summer
🍥 fish cake with swirl food japan sea beach narutomaki pink swirl kamaboko surimi ramen
🥮 moon cake food autumn
🍡 dango food dessert sweet japanese barbecue meat
🥟 dumpling food empanada pierogi potsticker
🥠 fortune cookie food prophecy
🥡 takeout box food leftovers
🦀 crab animal crustacean
🦞 lobster animal nature bisque claws seafood
🦐 shrimp animal ocean nature seafood
🦑 squid animal nature ocean sea
🦪 oyster food
🍦 soft ice cream food hot dessert summer
🍧 shaved ice hot dessert summer
🍨 ice cream food hot dessert
🍩 doughnut food dessert snack sweet donut
🍪 cookie food snack oreo chocolate sweet dessert
🎂 birthday cake food dessert cake
🍰 shortcake food dessert
🧁 cupcake food dessert bakery sweet
🥧 pie food dessert pastry
🍫 chocolate bar food snack dessert sweet
🍬 candy snack dessert sweet lolly
🍭 lollipop food snack candy sweet
🍮 custard dessert food
🍯 honey pot bees sweet kitchen
🍼 baby bottle food container milk
🥛 glass of milk beverage drink cow
☕ hot beverage beverage caffeine latte espresso coffee
🍵 teacup without handle drink bowl breakfast green british
🍶 sake wine drink drunk beverage japanese alcohol booze
🍾 bottle with popping cork drink wine bottle celebration
🍷 wine glass drink beverage drunk alcohol booze
🍸 cocktail glass drink drunk alcohol beverage booze mojito
🍹 tropical drink beverage cocktail summer beach alcohol booze mojito
🍺 beer mug relax beverage drink drunk party pub summer alcohol booze
🍻 clinking beer mugs relax beverage drink drunk party pub summer alcohol booze
🥂 clinking glasses beverage drink party alcohol celebrate cheers wine champagne toast
🥃 tumbler glass drink beverage drunk alcohol liquor booze bourbon scotch whisky glass shot
🥤 cup with straw drink soda
🧃 beverage box drink
🧉 mate drink tea beverage
🧊 ice water cold
🥢 chopsticks food
🍽️ fork and knife with plate food eat meal lunch dinner restaurant
🍴 fork and knife cutlery kitchen
🥄 spoon cutlery kitchen tableware
🔪 kitchen knife knife blade cutlery kitchen weapon
🏺 amphora vase jar
🌍 globe showing europe africa globe world international
🌎 globe showing americas globe world USA international
🌏 globe showing asia australia globe world east international
🌐 globe with meridians earth international world internet interweb i18n
🗺️ world map location direction
🗾 map of japan nation country japanese asia
🧭 compass magnetic navigation orienteering
🏔️ snow capped mountain photo nature environment winter cold
⛰️ mountain photo nature environment
🌋 volcano photo nature disaster
🗻 mount fuji photo mountain nature japanese
🏕️ camping photo outdoors tent
🏖️ beach with umbrella weather summer sunny sand mojito
🏜️ desert photo warm saharah
🏝️ desert island photo tropical mojito
🏞️ national park photo environment nature
🏟️ stadium photo place sports concert venue
🏛️ classical building art culture history
🏗️ building construction wip working progress
🧱 brick bricks
🏘️ houses buildings photo
🏚️ derelict house abandon evict broken building
🏠 house building home
🏡 house with garden home plant nature
🏢 office building building bureau work
🏣 japanese post office building envelope communication
🏤 post office building email
🏥 hospital building health surgery doctor
🏦 bank building money sales cash business enterprise
🏨 hotel building accomodation checkin
🏩 love hotel like affection dating
🏪 convenience store building shopping groceries
🏫 school building student education learn teach
🏬 department store building shopping mall
🏭 factory building industry pollution smoke
🏯 japanese castle photo building
🏰 castle building royalty history
💒 wedding love like affection couple marriage bride groom
🗼 tokyo tower photo japanese
🗽 statue of liberty american newyork
⛪ church building religion christ
🕌 mosque islam worship minaret
🛕 hindu temple religion
🕍 synagogue judaism worship temple jewish
⛩️ shinto shrine temple japan kyoto
🕋 kaaba mecca mosque islam
⛲ fountain photo summer water fresh
⛺ tent photo camping outdoors
🌁 foggy photo mountain
🌃 night with stars evening city downtown
🏙️ cityscape photo night life urban
🌄 sunrise over mountains view vacation photo
🌅 sunrise morning view vacation photo
🌆 cityscape at dusk photo evening sky buildings
🌇 sunset photo good morning dawn
🌉 bridge at night photo sanfrancisco
♨️ hot springs bath warm relax
🎠 carousel horse photo carnival
🎡 ferris wheel photo carnival londoneye
🎢 roller coaster carnival playground photo fun
💈 barber pole hair salon style
🎪 circus tent festival carnival party
🚂 locomotive transportation vehicle train
🚃 railway car transportation vehicle
🚄 high speed train transportation vehicle
🚅 bullet train transportation vehicle speed fast public travel
🚆 train transportation vehicle
🚇 metro transportation blue-square mrt underground tube
🚈 light rail transportation vehicle
🚉 station transportation vehicle public
🚊 tram transportation vehicle
🚝 monorail transportation vehicle
🚞 mountain railway transportation vehicle
🚋 tram car transportation vehicle carriage public travel
🚌 bus car vehicle transportation
🚍 oncoming bus vehicle transportation
🚎 trolleybus bart transportation vehicle
🚐 minibus vehicle car transportation
🚑 ambulance health 911 hospital
🚒 fire engine transportation cars vehicle
🚓 police car vehicle cars transportation law legal enforcement
🚔 oncoming police car vehicle law legal enforcement 911
🚕 taxi uber vehicle cars transportation
🚖 oncoming taxi vehicle cars uber
🚗 automobile red transportation vehicle
🚘 oncoming automobile car vehicle transportation
🚙 sport utility vehicle transportation vehicle
🚚 delivery truck cars transportation
🚛 articulated lorry vehicle cars transportation express
🚜 tractor vehicle car farming agriculture
🏎️ racing car sports race fast formula f1
🏍️ motorcycle race sports fast
🛵 motor scooter vehicle vespa sasha
🦽 manual wheelchair accessibility
🦼 motorized wheelchair accessibility
🛺 auto rickshaw move transportation
🚲 bicycle sports bicycle exercise hipster
🛴 kick scooter vehicle kick razor
🛹 skateboard board
🚏 bus stop transportation wait
🛣️ motorway road cupertino interstate highway
🛤️ railway track train transportation
🛢️ oil drum barrell
⛽ fuel pump gas station petroleum
🚨 police car light police ambulance 911 emergency alert error pinged law legal
🚥 horizontal traffic light transportation signal
🚦 vertical traffic light transportation driving
🛑 stop sign stop
🚧 construction wip progress caution warning
⚓ anchor ship ferry sea boat
⛵ sailboat ship summer transportation water sailing
🛶 canoe boat paddle water ship
🚤 speedboat ship transportation vehicle summer
🛳️ passenger ship yacht cruise ferry
⛴️ ferry boat ship yacht
🛥️ motor boat ship
🚢 ship transportation titanic deploy
✈️ airplane vehicle transportation flight fly
🛩️ small airplane flight transportation fly vehicle
🛫 airplane departure airport flight landing
🛬 airplane arrival airport flight boarding
🪂 parachute fly glide
💺 seat sit airplane transport bus flight fly
🚁 helicopter transportation vehicle fly
🚟 suspension railway vehicle transportation
🚠 mountain cableway transportation vehicle ski
🚡 aerial tramway transportation vehicle ski
🛰️ satellite communication gps orbit spaceflight NASA ISS
🚀 rocket launch ship staffmode NASA outer space outer space fly
🛸 flying saucer transportation vehicle ufo
🛎️ bellhop bell service
🧳 luggage packing travel
⌛ hourglass done time clock oldschool limit exam quiz test
⏳ hourglass not done oldschool time countdown
⌚ watch time accessories
⏰ alarm clock time wake
⏱️ stopwatch time deadline
⏲️ timer clock alarm
🕰️ mantelpiece clock time
🕛 twelve o clock time noon midnight midday late early schedule
🕧 twelve thirty time late early schedule
🕐 one o clock time late early schedule
🕜 one thirty time late early schedule
🕑 two o clock time late early schedule
🕝 two thirty time late early schedule
🕒 three o clock time late early schedule
🕞 three thirty time late early schedule
🕓 four o clock time late early schedule
🕟 four thirty time late early schedule
🕔 five o clock time late early schedule
🕠 five thirty time late early schedule
🕕 six o clock time late early schedule dawn dusk
🕡 six thirty time late early schedule
🕖 seven o clock time late early schedule
🕢 seven thirty time late early schedule
🕗 eight o clock time late early schedule
🕣 eight thirty time late early schedule
🕘 nine o clock time late early schedule
🕤 nine thirty time late early schedule
🕙 ten o clock time late early schedule
🕥 ten thirty time late early schedule
🕚 eleven o clock time late early schedule
🕦 eleven thirty time late early schedule
🌑 new moon nature twilight planet space night evening sleep
🌒 waxing crescent moon nature twilight planet space night evening sleep
🌓 first quarter moon nature twilight planet space night evening sleep
🌔 waxing gibbous moon nature night sky gray twilight planet space evening sleep
🌕 full moon nature yellow twilight planet space night evening sleep
🌖 waning gibbous moon nature twilight planet space night evening sleep waxing gibbous moon
🌗 last quarter moon nature twilight planet space night evening sleep
🌘 waning crescent moon nature twilight planet space night evening sleep
🌙 crescent moon night sleep sky evening magic
🌚 new moon face nature twilight planet space night evening sleep
🌛 first quarter moon face nature twilight planet space night evening sleep
🌜 last quarter moon face nature twilight planet space night evening sleep
🌡️ thermometer weather temperature hot cold
☀️ sun weather nature brightness summer beach spring
🌝 full moon face nature twilight planet space night evening sleep
🌞 sun with face nature morning sky
🪐 ringed planet outerspace
⭐ star night yellow
🌟 glowing star night sparkle awesome good magic
🌠 shooting star night photo
🌌 milky way photo space stars
☁️ cloud weather sky
⛅ sun behind cloud weather nature cloudy morning fall spring
⛈️ cloud with lightning and rain weather lightning
🌤️ sun behind small cloud weather
🌥️ sun behind large cloud weather
🌦️ sun behind rain cloud weather
🌧️ cloud with rain weather
🌨️ cloud with snow weather
🌩️ cloud with lightning weather thunder
🌪️ tornado weather cyclone twister
🌫️ fog weather
🌬️ wind face gust air
🌀 cyclone weather swirl blue cloud vortex spiral whirlpool spin tornado hurricane typhoon
🌈 rainbow nature happy unicorn face photo sky spring
🌂 closed umbrella weather rain drizzle
☂️ umbrella weather spring
☔ umbrella with rain drops rainy weather spring
⛱️ umbrella on ground weather summer
⚡ high voltage thunder weather lightning bolt fast
❄️ snowflake winter season cold weather christmas xmas
☃️ snowman winter season cold weather christmas xmas frozen
⛄ snowman without snow winter season cold weather christmas xmas frozen without snow
☄️ comet space
🔥 fire hot cook flame
💧 droplet water drip faucet spring
🌊 water wave sea water wave nature tsunami disaster
🎃 jack o lantern halloween light pumpkin creepy fall
🎄 christmas tree festival vacation december xmas celebration
🎆 fireworks photo festival carnival congratulations
🎇 sparkler stars night shine
🧨 firecracker dynamite boom explode explosion explosive
✨ sparkles stars shine shiny cool awesome good magic
🎈 balloon party celebration birthday circus
🎉 party popper party congratulations birthday magic circus celebration tada
🎊 confetti ball festival party birthday circus
🎋 tanabata tree plant nature branch summer
🎍 pine decoration plant nature vegetable panda pine decoration
🎎 japanese dolls japanese toy kimono
🎏 carp streamer fish japanese koinobori carp banner
🎐 wind chime nature ding spring bell
🎑 moon viewing ceremony photo japan asia tsukimi
🧧 red envelope gift
🎀 ribbon decoration pink girl bowtie
🎁 wrapped gift present birthday christmas xmas
🎗️ reminder ribbon sports cause support awareness
🎟️ admission tickets sports concert entrance
🎫 ticket event concert pass
🎖️ military medal award winning army
🏆 trophy win award contest place ftw ceremony
🏅 sports medal award winning
🥇 1st place medal award winning first
🥈 2nd place medal award second
🥉 3rd place medal award third
⚽ soccer ball sports football
⚾ baseball sports balls
🥎 softball sports balls
🏀 basketball sports balls NBA
🏐 volleyball sports balls
🏈 american football sports balls NFL
🏉 rugby football sports team
🎾 tennis sports balls green
🥏 flying disc sports frisbee ultimate
🎳 bowling sports fun play
🏏 cricket game sports
🏑 field hockey sports
🏒 ice hockey sports
🥍 lacrosse sports ball stick
🏓 ping pong sports pingpong
🏸 badminton sports
🥊 boxing glove sports fighting
🥋 martial arts uniform judo karate taekwondo
🥅 goal net sports
⛳ flag in hole sports business flag hole summer
⛸️ ice skate sports
🎣 fishing pole food hobby summer
🤿 diving mask sport ocean
🎽 running shirt play pageant
🎿 skis sports winter cold snow
🛷 sled sleigh luge toboggan
🥌 curling stone sports
🎯 direct hit game play bar target bullseye
🪀 yo yo toy
🪁 kite wind fly
🎱 pool 8 ball pool hobby game luck magic
🔮 crystal ball disco party magic circus fortune teller
🧿 nazar amulet bead charm
🎮 video game play console PS4 controller
🕹️ joystick game play
🎰 slot machine bet gamble vegas fruit machine luck casino
🎲 game die dice random tabletop play luck
🧩 puzzle piece interlocking puzzle piece
🧸 teddy bear plush stuffed
♠️ spade suit poker cards suits magic
♥️ heart suit poker cards magic suits
♦️ diamond suit poker cards magic suits
♣️ club suit poker cards magic suits
♟️ chess pawn expendable
🃏 joker poker cards game play magic
🀄 mahjong red dragon game play chinese kanji
🎴 flower playing cards game sunset red
🎭 performing arts acting theater drama
🖼️ framed picture photography
🎨 artist palette design paint draw colors
🧵 thread needle sewing spool string
🧶 yarn ball crochet knit
👓 glasses fashion accessories eyesight nerdy dork geek
🕶️ sunglasses face cool accessories
🥽 goggles eyes protection safety
🥼 lab coat doctor experiment scientist chemist
🦺 safety vest protection
👔 necktie shirt suitup formal fashion cloth business
👕 t shirt fashion cloth casual shirt tee
👖 jeans fashion shopping
🧣 scarf neck winter clothes
🧤 gloves hands winter clothes
🧥 coat jacket
🧦 socks stockings clothes
👗 dress clothes fashion shopping
👘 kimono dress fashion women female japanese
🥻 sari dress
🩱 one piece swimsuit fashion
🩲 briefs clothing
🩳 shorts clothing
👙 bikini swimming female woman girl fashion beach summer
👚 woman s clothes fashion shopping bags female
👛 purse fashion accessories money sales shopping
👜 handbag fashion accessory accessories shopping
👝 clutch bag bag accessories shopping
🛍️ shopping bags mall buy purchase
🎒 backpack student education bag backpack
👞 man s shoe fashion male
👟 running shoe shoes sports sneakers
🥾 hiking boot backpacking camping hiking
🥿 flat shoe ballet slip-on slipper
👠 high heeled shoe fashion shoes female pumps stiletto
👡 woman s sandal shoes fashion flip flops
🩰 ballet shoes dance
👢 woman s boot shoes fashion
👑 crown king kod leader royalty lord
👒 woman s hat fashion accessories female lady spring
🎩 top hat magic gentleman classy circus
🎓 graduation cap school college degree university graduation cap hat legal learn education
🧢 billed cap cap baseball
⛑️ rescue worker s helmet construction build
📿 prayer beads dhikr religious
💄 lipstick female girl fashion woman
💍 ring wedding propose marriage valentines diamond fashion jewelry gem engagement
💎 gem stone blue ruby diamond jewelry
🔇 muted speaker sound volume silence quiet
🔈 speaker low volume sound volume silence broadcast
🔉 speaker medium volume volume speaker broadcast
🔊 speaker high volume volume noise noisy speaker broadcast
📢 loudspeaker volume sound
📣 megaphone sound speaker volume
📯 postal horn instrument music
🔔 bell sound notification christmas xmas chime
🔕 bell with slash sound volume mute quiet silent
🎼 musical score treble clef compose
🎵 musical note score tone sound
🎶 musical notes music score
🎙️ studio microphone sing recording artist talkshow
🎚️ level slider scale
🎛️ control knobs dial
🎤 microphone sound music PA sing talkshow
🎧 headphone music score gadgets
📻 radio communication music podcast program
🎷 saxophone music instrument jazz blues
🎸 guitar music instrument
🎹 musical keyboard piano instrument compose
🎺 trumpet music brass
🎻 violin music instrument orchestra symphony
🪕 banjo music instructment
🥁 drum music instrument drumsticks snare
📱 mobile phone technology apple gadgets dial
📲 mobile phone with arrow iphone incoming
☎️ telephone technology communication dial telephone
📞 telephone receiver technology communication dial
📟 pager bbcall oldschool 90s
📠 fax machine communication technology
🔋 battery power energy sustain
🔌 electric plug charger power
💻 laptop technology laptop screen display monitor
🖥️ desktop computer technology computing screen
🖨️ printer paper ink
⌨️ keyboard technology computer type input text
🖱️ computer mouse click
🖲️ trackball technology trackpad
💽 computer disk technology record data disk 90s
💾 floppy disk oldschool technology save 90s 80s
💿 optical disk technology dvd disk disc 90s
📀 dvd cd disk disc
🧮 abacus calculation
🎥 movie camera film record
🎞️ film frames movie
📽️ film projector video tape record movie
🎬 clapper board movie film record
📺 television technology program oldschool show television
📷 camera gadgets photography
📸 camera with flash photography gadgets
📹 video camera film record
📼 videocassette record video oldschool 90s 80s
🔍 magnifying glass tilted left search zoom find detective
🔎 magnifying glass tilted right search zoom find detective
🕯️ candle fire wax
💡 light bulb light electricity idea
🔦 flashlight dark camping sight night
🏮 red paper lantern light paper halloween spooky
🪔 diya lamp lighting
📔 notebook with decorative cover classroom notes record paper study
📕 closed book read library knowledge textbook learn
📖 open book book read library knowledge literature learn study
📗 green book read library knowledge study
📘 blue book read library knowledge learn study
📙 orange book read library knowledge textbook study
📚 books literature library study
📓 notebook stationery record notes paper study
📒 ledger notes paper
📃 page with curl documents office paper
📜 scroll documents ancient history paper
📄 page facing up documents office paper information
📰 newspaper press headline
🗞️ rolled up newspaper press headline
📑 bookmark tabs favorite save order tidy
🔖 bookmark favorite label save
🏷️ label sale tag
💰 money bag dollar payment coins sale
💴 yen banknote money sales japanese dollar currency
💵 dollar banknote money sales bill currency
💶 euro banknote money sales dollar currency
💷 pound banknote british sterling money sales bills uk england currency
💸 money with wings dollar bills payment sale
💳 credit card money sales dollar bill payment shopping
🧾 receipt accounting expenses
💹 chart increasing with yen green-square graph presentation stats
💱 currency exchange money sales dollar travel
💲 heavy dollar sign money sales payment currency buck
✉️ envelope letter postal inbox communication
📧 e mail communication inbox
📨 incoming envelope email inbox
📩 envelope with arrow email communication
📤 outbox tray inbox email
📥 inbox tray email documents
📦 package mail gift cardboard box moving
📫 closed mailbox with raised flag email inbox communication
📪 closed mailbox with lowered flag email communication inbox
📬 open mailbox with raised flag email inbox communication
📭 open mailbox with lowered flag email inbox
📮 postbox email letter envelope
🗳️ ballot box with ballot election vote
✏️ pencil stationery write paper writing school study
✒️ black nib pen stationery writing write
🖋️ fountain pen stationery writing write
🖊️ pen stationery writing write
🖌️ paintbrush drawing creativity art
🖍️ crayon drawing creativity
📝 memo write documents stationery pencil paper writing legal exam quiz test study compose
💼 briefcase business documents work law legal job career
📁 file folder documents business office
📂 open file folder documents load
🗂️ card index dividers organizing business stationery
📅 calendar calendar schedule
📆 tear off calendar schedule date planning
🗒️ spiral notepad memo stationery
🗓️ spiral calendar date schedule planning
📇 card index business stationery
📈 chart increasing graph presentation stats recovery business economics money sales good success
📉 chart decreasing graph presentation stats recession business economics money sales bad failure
📊 bar chart graph presentation stats
📋 clipboard stationery documents
📌 pushpin stationery mark here
📍 round pushpin stationery location map here
📎 paperclip documents stationery
🖇️ linked paperclips documents stationery
📏 straight ruler stationery calculate length math school drawing architect sketch
📐 triangular ruler stationery math architect sketch
✂️ scissors stationery cut
🗃️ card file box business stationery
🗄️ file cabinet filing organizing
🗑️ wastebasket bin trash rubbish garbage toss
🔒 locked security password padlock
🔓 unlocked privacy security
🔏 locked with pen security secret
🔐 locked with key security privacy
🔑 key lock door password
🗝️ old key lock door password
🔨 hammer tools build create
🪓 axe tool chop cut
⛏️ pick tools dig
⚒️ hammer and pick tools build create
🛠️ hammer and wrench tools build create
🗡️ dagger weapon
⚔️ crossed swords weapon
🔫 pistol violence weapon pistol revolver
🏹 bow and arrow sports
🛡️ shield protection security
🔧 wrench tools diy ikea fix maintainer
🔩 nut and bolt handy tools fix
⚙️ gear cog
🗜️ clamp tool
⚖️ balance scale law fairness weight
🦯 probing cane accessibility
🔗 link rings url
⛓️ chains lock arrest
🧰 toolbox tools diy fix maintainer mechanic
🧲 magnet attraction magnetic
⚗️ alembic distilling science experiment chemistry
🧪 test tube chemistry experiment lab science
🧫 petri dish bacteria biology culture lab
🧬 dna biologist genetics life
🔬 microscope laboratory experiment zoomin science study
🔭 telescope stars space zoom science astronomy
📡 satellite antenna communication future radio space
💉 syringe health hospital drugs blood medicine needle doctor nurse
🩸 drop of blood period hurt harm wound
💊 pill health medicine doctor pharmacy drug
🩹 adhesive bandage heal
🩺 stethoscope health
🚪 door house entry exit
🛏️ bed sleep rest
🛋️ couch and lamp read chill
🪑 chair sit furniture
🚽 toilet restroom wc washroom bathroom potty
🚿 shower clean water bathroom
🛁 bathtub clean shower bathroom
🪒 razor cut
🧴 lotion bottle moisturizer sunscreen
🧷 safety pin diaper
🧹 broom cleaning sweeping witch
🧺 basket laundry
🧻 roll of paper roll
🧼 soap bar bathing cleaning lather
🧽 sponge absorbing cleaning porous
🧯 fire extinguisher quench
🛒 shopping cart trolley
🚬 cigarette kills tobacco cigarette joint smoke
⚰️ coffin vampire dead die death rip graveyard cemetery casket funeral box
⚱️ funeral urn dead die death rip ashes
🗿 moai rock easter island moai
🏧 atm sign money sales cash blue-square payment bank
🚮 litter in bin sign blue-square sign human info
🚰 potable water blue-square liquid restroom cleaning faucet
♿ wheelchair symbol blue-square disabled accessibility
🚹 men s room toilet restroom wc blue-square gender male
🚺 women s room purple-square woman female toilet loo restroom gender
🚻 restroom blue-square toilet refresh wc gender
🚼 baby symbol orange-square child
🚾 water closet toilet restroom blue-square
🛂 passport control custom blue-square
🛃 customs passport border blue-square
🛄 baggage claim blue-square airport transport
🛅 left luggage blue-square travel
⚠️ warning exclamation wip alert error problem issue
🚸 children crossing school warning danger sign driving yellow-diamond
⛔ no entry limit security privacy bad denied stop circle
🚫 prohibited forbid stop limit denied disallow circle
🚳 no bicycles cyclist prohibited circle
🚭 no smoking cigarette blue-square smell smoke
🚯 no littering trash bin garbage circle
🚱 non potable water drink faucet tap circle
🚷 no pedestrians rules crossing walking circle
📵 no mobile phones iphone mute circle
🔞 no one under eighteen 18 drink pub night minor circle
☢️ radioactive nuclear danger
☣️ biohazard danger
⬆️ up arrow blue-square continue top direction
↗️ up right arrow blue-square point direction diagonal northeast
➡️ right arrow blue-square next
↘️ down right arrow blue-square direction diagonal southeast
⬇️ down arrow blue-square direction bottom
↙️ down left arrow blue-square direction diagonal southwest
⬅️ left arrow blue-square previous back
↖️ up left arrow blue-square point direction diagonal northwest
↕️ up down arrow blue-square direction way vertical
↔️ left right arrow shape direction horizontal sideways
↩️ right arrow curving left back return blue-square undo enter
↪️ left arrow curving right blue-square return rotate direction
⤴️ right arrow curving up blue-square direction top
⤵️ right arrow curving down blue-square direction bottom
🔃 clockwise vertical arrows sync cycle round repeat
🔄 counterclockwise arrows button blue-square sync cycle
🔙 back arrow arrow words return
🔚 end arrow words arrow
🔛 on arrow arrow words
🔜 soon arrow arrow words
🔝 top arrow words blue-square
🛐 place of worship religion church temple prayer
⚛️ atom symbol science physics chemistry
🕉️ om hinduism buddhism sikhism jainism
✡️ star of david judaism
☸️ wheel of dharma hinduism buddhism sikhism jainism
☯️ yin yang balance
✝️ latin cross christianity
☦️ orthodox cross suppedaneum religion
☪️ star and crescent islam
☮️ peace symbol hippie
🕎 menorah hanukkah candles jewish
🔯 dotted six pointed star purple-square religion jewish hexagram
♈ aries sign purple-square zodiac astrology
♉ taurus purple-square sign zodiac astrology
♊ gemini sign zodiac purple-square astrology
♋ cancer sign zodiac purple-square astrology
♌ leo sign purple-square zodiac astrology
♍ virgo sign zodiac purple-square astrology
♎ libra sign purple-square zodiac astrology
♏ scorpio sign zodiac purple-square astrology scorpio
♐ sagittarius sign zodiac purple-square astrology
♑ capricorn sign zodiac purple-square astrology
♒ aquarius sign purple-square zodiac astrology
♓ pisces purple-square sign zodiac astrology
⛎ ophiuchus sign purple-square constellation astrology
🔀 shuffle tracks button blue-square shuffle music random
🔁 repeat button loop record
🔂 repeat single button blue-square loop
▶️ play button blue-square right direction play
⏩ fast forward button blue-square play speed continue
⏭️ next track button forward next blue-square
⏯️ play or pause button blue-square play pause
◀️ reverse button blue-square left direction
⏪ fast reverse button play blue-square
⏮️ last track button backward
🔼 upwards button blue-square triangle direction point forward top
⏫ fast up button blue-square direction top
🔽 downwards button blue-square direction bottom
⏬ fast down button blue-square direction bottom
⏸️ pause button pause blue-square
⏹️ stop button blue-square
⏺️ record button blue-square
⏏️ eject button blue-square
🎦 cinema blue-square record film movie curtain stage theater
🔅 dim button sun afternoon warm summer
🔆 bright button sun light
📶 antenna bars blue-square reception phone internet connection wifi bluetooth bars
📳 vibration mode orange-square phone
📴 mobile phone off mute orange-square silence quiet
♀️ female sign woman women lady girl
♂️ male sign man boy men
⚕️ medical symbol health hospital
♾️ infinity forever
♻️ recycling symbol arrow environment garbage trash
⚜️ fleur de lis decorative scout
🔱 trident emblem weapon spear
📛 name badge fire forbid
🔰 japanese symbol for beginner badge shield
⭕ hollow red circle circle round
✅ check mark button green-square ok agree vote election answer tick
☑️ check box with check ok agree confirm black-square vote election yes tick
✔️ check mark ok nike answer yes tick
✖️ multiplication sign math calculation
❌ cross mark no delete remove cancel red
❎ cross mark button x green-square no deny
➕ plus sign math calculation addition more increase
➖ minus sign math calculation subtract less
➗ division sign divide math calculation
➰ curly loop scribble draw shape squiggle
➿ double curly loop tape cassette
〽️ part alternation mark graph presentation stats business economics bad
✳️ eight spoked asterisk star sparkle green-square
✴️ eight pointed star orange-square shape polygon
❇️ sparkle stars green-square awesome good fireworks
‼️ double exclamation mark exclamation surprise
⁉️ exclamation question mark wat punctuation surprise
❓ question mark doubt confused
❔ white question mark doubts gray huh confused
❕ white exclamation mark surprise punctuation gray wow warning
❗ exclamation mark heavy exclamation mark danger surprise punctuation wow warning
〰️ wavy dash draw line moustache mustache squiggle scribble
©️ copyright ip license circle law legal
®️ registered alphabet circle
™️ trade mark trademark brand law legal
#️⃣ keycap  symbol blue-square twitter
*️⃣ keycap  star keycap
0️⃣ keycap 0 0 numbers blue-square null
1️⃣ keycap 1 blue-square numbers 1
2️⃣ keycap 2 numbers 2 prime blue-square
3️⃣ keycap 3 3 numbers prime blue-square
4️⃣ keycap 4 4 numbers blue-square
5️⃣ keycap 5 5 numbers blue-square prime
6️⃣ keycap 6 6 numbers blue-square
7️⃣ keycap 7 7 numbers blue-square prime
8️⃣ keycap 8 8 blue-square numbers
9️⃣ keycap 9 blue-square numbers 9
🔟 keycap 10 numbers 10 blue-square
🔠 input latin uppercase alphabet words blue-square
🔡 input latin lowercase blue-square alphabet
🔢 input numbers numbers blue-square
🔣 input symbols blue-square music note ampersand percent glyphs characters
🔤 input latin letters blue-square alphabet
🅰️ a button red-square alphabet letter
🆎 ab button red-square alphabet
🅱️ b button red-square alphabet letter
🆑 cl button alphabet words red-square
🆒 cool button words blue-square
🆓 free button blue-square words
ℹ️ information blue-square alphabet letter
🆔 id button purple-square words
Ⓜ️ circled m alphabet blue-circle letter
🆕 new button blue-square words start
🆖 ng button blue-square words shape icon
🅾️ o button alphabet red-square letter
🆗 ok button good agree yes blue-square
🅿️ p button cars blue-square alphabet letter
🆘 sos button help red-square words emergency 911
🆙 up button blue-square above high
🆚 vs button words orange-square
🈁 japanese here button blue-square here katakana japanese destination
🈂️ japanese service charge button japanese blue-square katakana
🈷️ japanese monthly amount button chinese month moon japanese orange-square kanji
🈶 japanese not free of charge button orange-square chinese have kanji
🈯 japanese reserved button chinese point green-square kanji
🉐 japanese bargain button chinese kanji obtain get circle
🈹 japanese discount button cut divide chinese kanji pink-square
🈚 japanese free of charge button nothing chinese kanji japanese orange-square
🈲 japanese prohibited button kanji japanese chinese forbidden limit restricted red-square
🉑 japanese acceptable button ok good chinese kanji agree yes orange-circle
🈸 japanese application button chinese japanese kanji orange-square
🈴 japanese passing grade button japanese chinese join kanji red-square
🈳 japanese vacancy button kanji japanese chinese empty sky blue-square
㊗️ japanese congratulations button chinese kanji japanese red-circle
㊙️ japanese secret button privacy chinese sshh kanji red-circle
🈺 japanese open for business button japanese opening hours orange-square
🈵 japanese no vacancy button full chinese japanese red-square kanji
🔴 red circle shape error danger
🟠 orange circle round
🟡 yellow circle round
🟢 green circle round
🔵 blue circle shape icon button
🟣 purple circle round
🟤 brown circle round
⚫ black circle shape button round
⚪ white circle shape round
🟥 red square
🟧 orange square
🟨 yellow square
🟩 green square
🟦 blue square
🟪 purple square
🟫 brown square
⬛ black large square shape icon button
⬜ white large square shape icon stone button
◼️ black medium square shape button icon
◻️ white medium square shape stone icon
◾ black medium small square icon shape button
◽ white medium small square shape stone icon button
▪️ black small square shape icon
▫️ white small square shape icon
🔶 large orange diamond shape jewel gem
🔷 large blue diamond shape jewel gem
🔸 small orange diamond shape jewel gem
🔹 small blue diamond shape jewel gem
🔺 red triangle pointed up shape direction up top
🔻 red triangle pointed down shape direction bottom
💠 diamond with a dot jewel blue gem crystal fancy
🔘 radio button input old music circle
🔳 white square button shape input
🔲 black square button shape input frame
🏁 chequered flag contest finishline race gokart
🚩 triangular flag mark milestone place
🎌 crossed flags japanese nation country border
🏴 black flag pirate
🏳️ white flag losing loser lost surrender give up fail
🏳️‍🌈 rainbow flag flag rainbow pride gay lgbt glbt queer homosexual lesbian bisexual transgender
🏴‍☠️ pirate flag skull crossbones flag banner
🇦🇨 flag ascension island
🇦🇩 flag andorra ad flag nation country banner andorra
🇦🇪 flag united arab emirates united arab emirates flag nation country banner united arab emirates
🇦🇫 flag afghanistan af flag nation country banner afghanistan
🇦🇬 flag antigua barbuda antigua barbuda flag nation country banner antigua barbuda
🇦🇮 flag anguilla ai flag nation country banner anguilla
🇦🇱 flag albania al flag nation country banner albania
🇦🇲 flag armenia am flag nation country banner armenia
🇦🇴 flag angola ao flag nation country banner angola
🇦🇶 flag antarctica aq flag nation country banner antarctica
🇦🇷 flag argentina ar flag nation country banner argentina
🇦🇸 flag american samoa american ws flag nation country banner american samoa
🇦🇹 flag austria at flag nation country banner austria
🇦🇺 flag australia au flag nation country banner australia
🇦🇼 flag aruba aw flag nation country banner aruba
🇦🇽 flag aland islands Åland islands flag nation country banner aland islands
🇦🇿 flag azerbaijan az flag nation country banner azerbaijan
🇧🇦 flag bosnia herzegovina bosnia herzegovina flag nation country banner bosnia herzegovina
🇧🇧 flag barbados bb flag nation country banner barbados
🇧🇩 flag bangladesh bd flag nation country banner bangladesh
🇧🇪 flag belgium be flag nation country banner belgium
🇧🇫 flag burkina faso burkina faso flag nation country banner burkina faso
🇧🇬 flag bulgaria bg flag nation country banner bulgaria
🇧🇭 flag bahrain bh flag nation country banner bahrain
🇧🇮 flag burundi bi flag nation country banner burundi
🇧🇯 flag benin bj flag nation country banner benin
🇧🇱 flag st barthelemy saint barthélemy flag nation country banner st barthelemy
🇧🇲 flag bermuda bm flag nation country banner bermuda
🇧🇳 flag brunei bn darussalam flag nation country banner brunei
🇧🇴 flag bolivia bo flag nation country banner bolivia
🇧🇶 flag caribbean netherlands bonaire flag nation country banner caribbean netherlands
🇧🇷 flag brazil br flag nation country banner brazil
🇧🇸 flag bahamas bs flag nation country banner bahamas
🇧🇹 flag bhutan bt flag nation country banner bhutan
🇧🇻 flag bouvet island norway
🇧🇼 flag botswana bw flag nation country banner botswana
🇧🇾 flag belarus by flag nation country banner belarus
🇧🇿 flag belize bz flag nation country banner belize
🇨🇦 flag canada ca flag nation country banner canada
🇨🇨 flag cocos islands cocos keeling islands flag nation country banner cocos islands
🇨🇩 flag congo kinshasa congo democratic republic flag nation country banner congo kinshasa
🇨🇫 flag central african republic central african republic flag nation country banner central african republic
🇨🇬 flag congo brazzaville congo flag nation country banner congo brazzaville
🇨🇭 flag switzerland ch flag nation country banner switzerland
🇨🇮 flag cote d ivoire ivory coast flag nation country banner cote d ivoire
🇨🇰 flag cook islands cook islands flag nation country banner cook islands
🇨🇱 flag chile flag nation country banner chile
🇨🇲 flag cameroon cm flag nation country banner cameroon
🇨🇳 flag china china chinese prc flag country nation banner china
🇨🇴 flag colombia co flag nation country banner colombia
🇨🇵 flag clipperton island
🇨🇷 flag costa rica costa rica flag nation country banner costa rica
🇨🇺 flag cuba cu flag nation country banner cuba
🇨🇻 flag cape verde cabo verde flag nation country banner cape verde
🇨🇼 flag curacao curaçao flag nation country banner curacao
🇨🇽 flag christmas island christmas island flag nation country banner christmas island
🇨🇾 flag cyprus cy flag nation country banner cyprus
🇨🇿 flag czechia cz flag nation country banner czechia
🇩🇪 flag germany german nation flag country banner germany
🇩🇬 flag diego garcia
🇩🇯 flag djibouti dj flag nation country banner djibouti
🇩🇰 flag denmark dk flag nation country banner denmark
🇩🇲 flag dominica dm flag nation country banner dominica
🇩🇴 flag dominican republic dominican republic flag nation country banner dominican republic
🇩🇿 flag algeria dz flag nation country banner algeria
🇪🇦 flag ceuta melilla
🇪🇨 flag ecuador ec flag nation country banner ecuador
🇪🇪 flag estonia ee flag nation country banner estonia
🇪🇬 flag egypt eg flag nation country banner egypt
🇪🇭 flag western sahara western sahara flag nation country banner western sahara
🇪🇷 flag eritrea er flag nation country banner eritrea
🇪🇸 flag spain spain flag nation country banner spain
🇪🇹 flag ethiopia et flag nation country banner ethiopia
🇪🇺 flag european union european union flag banner
🇫🇮 flag finland fi flag nation country banner finland
🇫🇯 flag fiji fj flag nation country banner fiji
🇫🇰 flag falkland islands falkland islands malvinas flag nation country banner falkland islands
🇫🇲 flag micronesia micronesia federated states flag nation country banner micronesia
🇫🇴 flag faroe islands faroe islands flag nation country banner faroe islands
🇫🇷 flag france banner flag nation france french country france
🇬🇦 flag gabon ga flag nation country banner gabon
🇬🇧 flag united kingdom united kingdom great britain northern ireland flag nation country banner british UK english england union jack united kingdom
🇬🇩 flag grenada gd flag nation country banner grenada
🇬🇪 flag georgia ge flag nation country banner georgia
🇬🇫 flag french guiana french guiana flag nation country banner french guiana
🇬🇬 flag guernsey gg flag nation country banner guernsey
🇬🇭 flag ghana gh flag nation country banner ghana
🇬🇮 flag gibraltar gi flag nation country banner gibraltar
🇬🇱 flag greenland gl flag nation country banner greenland
🇬🇲 flag gambia gm flag nation country banner gambia
🇬🇳 flag guinea gn flag nation country banner guinea
🇬🇵 flag guadeloupe gp flag nation country banner guadeloupe
🇬🇶 flag equatorial guinea equatorial gn flag nation country banner equatorial guinea
🇬🇷 flag greece gr flag nation country banner greece
🇬🇸 flag south georgia south sandwich islands south georgia sandwich islands flag nation country banner south georgia south sandwich islands
🇬🇹 flag guatemala gt flag nation country banner guatemala
🇬🇺 flag guam gu flag nation country banner guam
🇬🇼 flag guinea bissau gw bissau flag nation country banner guinea bissau
🇬🇾 flag guyana gy flag nation country banner guyana
🇭🇰 flag hong kong sar china hong kong flag nation country banner hong kong sar china
🇭🇲 flag heard mcdonald islands
🇭🇳 flag honduras hn flag nation country banner honduras
🇭🇷 flag croatia hr flag nation country banner croatia
🇭🇹 flag haiti ht flag nation country banner haiti
🇭🇺 flag hungary hu flag nation country banner hungary
🇮🇨 flag canary islands canary islands flag nation country banner canary islands
🇮🇩 flag indonesia flag nation country banner indonesia
🇮🇪 flag ireland ie flag nation country banner ireland
🇮🇱 flag israel il flag nation country banner israel
🇮🇲 flag isle of man isle man flag nation country banner isle of man
🇮🇳 flag india in flag nation country banner india
🇮🇴 flag british indian ocean territory british indian ocean territory flag nation country banner british indian ocean territory
🇮🇶 flag iraq iq flag nation country banner iraq
🇮🇷 flag iran iran islamic republic flag nation country banner iran
🇮🇸 flag iceland is flag nation country banner iceland
🇮🇹 flag italy italy flag nation country banner italy
🇯🇪 flag jersey je flag nation country banner jersey
🇯🇲 flag jamaica jm flag nation country banner jamaica
🇯🇴 flag jordan jo flag nation country banner jordan
🇯🇵 flag japan japanese nation flag country banner japan
🇰🇪 flag kenya ke flag nation country banner kenya
🇰🇬 flag kyrgyzstan kg flag nation country banner kyrgyzstan
🇰🇭 flag cambodia kh flag nation country banner cambodia
🇰🇮 flag kiribati ki flag nation country banner kiribati
🇰🇲 flag comoros km flag nation country banner comoros
🇰🇳 flag st kitts nevis saint kitts nevis flag nation country banner st kitts nevis
🇰🇵 flag north korea north korea nation flag country banner north korea
🇰🇷 flag south korea south korea nation flag country banner south korea
🇰🇼 flag kuwait kw flag nation country banner kuwait
🇰🇾 flag cayman islands cayman islands flag nation country banner cayman islands
🇰🇿 flag kazakhstan kz flag nation country banner kazakhstan
🇱🇦 flag laos lao democratic republic flag nation country banner laos
🇱🇧 flag lebanon lb flag nation country banner lebanon
🇱🇨 flag st lucia saint lucia flag nation country banner st lucia
🇱🇮 flag liechtenstein li flag nation country banner liechtenstein
🇱🇰 flag sri lanka sri lanka flag nation country banner sri lanka
🇱🇷 flag liberia lr flag nation country banner liberia
🇱🇸 flag lesotho ls flag nation country banner lesotho
🇱🇹 flag lithuania lt flag nation country banner lithuania
🇱🇺 flag luxembourg lu flag nation country banner luxembourg
🇱🇻 flag latvia lv flag nation country banner latvia
🇱🇾 flag libya ly flag nation country banner libya
🇲🇦 flag morocco ma flag nation country banner morocco
🇲🇨 flag monaco mc flag nation country banner monaco
🇲🇩 flag moldova moldova republic flag nation country banner moldova
🇲🇪 flag montenegro me flag nation country banner montenegro
🇲🇫 flag st martin
🇲🇬 flag madagascar mg flag nation country banner madagascar
🇲🇭 flag marshall islands marshall islands flag nation country banner marshall islands
🇲🇰 flag north macedonia macedonia flag nation country banner north macedonia
🇲🇱 flag mali ml flag nation country banner mali
🇲🇲 flag myanmar mm flag nation country banner myanmar
🇲🇳 flag mongolia mn flag nation country banner mongolia
🇲🇴 flag macao sar china macao flag nation country banner macao sar china
🇲🇵 flag northern mariana islands northern mariana islands flag nation country banner northern mariana islands
🇲🇶 flag martinique mq flag nation country banner martinique
🇲🇷 flag mauritania mr flag nation country banner mauritania
🇲🇸 flag montserrat ms flag nation country banner montserrat
🇲🇹 flag malta mt flag nation country banner malta
🇲🇺 flag mauritius mu flag nation country banner mauritius
🇲🇻 flag maldives mv flag nation country banner maldives
🇲🇼 flag malawi mw flag nation country banner malawi
🇲🇽 flag mexico mx flag nation country banner mexico
🇲🇾 flag malaysia my flag nation country banner malaysia
🇲🇿 flag mozambique mz flag nation country banner mozambique
🇳🇦 flag namibia na flag nation country banner namibia
🇳🇨 flag new caledonia new caledonia flag nation country banner new caledonia
🇳🇪 flag niger ne flag nation country banner niger
🇳🇫 flag norfolk island norfolk island flag nation country banner norfolk island
🇳🇬 flag nigeria flag nation country banner nigeria
🇳🇮 flag nicaragua ni flag nation country banner nicaragua
🇳🇱 flag netherlands nl flag nation country banner netherlands
🇳🇴 flag norway no flag nation country banner norway
🇳🇵 flag nepal np flag nation country banner nepal
🇳🇷 flag nauru nr flag nation country banner nauru
🇳🇺 flag niue nu flag nation country banner niue
🇳🇿 flag new zealand new zealand flag nation country banner new zealand
🇴🇲 flag oman om symbol flag nation country banner oman
🇵🇦 flag panama pa flag nation country banner panama
🇵🇪 flag peru pe flag nation country banner peru
🇵🇫 flag french polynesia french polynesia flag nation country banner french polynesia
🇵🇬 flag papua new guinea papua new guinea flag nation country banner papua new guinea
🇵🇭 flag philippines ph flag nation country banner philippines
🇵🇰 flag pakistan pk flag nation country banner pakistan
🇵🇱 flag poland pl flag nation country banner poland
🇵🇲 flag st pierre miquelon saint pierre miquelon flag nation country banner st pierre miquelon
🇵🇳 flag pitcairn islands pitcairn flag nation country banner pitcairn islands
🇵🇷 flag puerto rico puerto rico flag nation country banner puerto rico
🇵🇸 flag palestinian territories palestine palestinian territories flag nation country banner palestinian territories
🇵🇹 flag portugal pt flag nation country banner portugal
🇵🇼 flag palau pw flag nation country banner palau
🇵🇾 flag paraguay py flag nation country banner paraguay
🇶🇦 flag qatar qa flag nation country banner qatar
🇷🇪 flag reunion réunion flag nation country banner reunion
🇷🇴 flag romania ro flag nation country banner romania
🇷🇸 flag serbia rs flag nation country banner serbia
🇷🇺 flag russia russian federation flag nation country banner russia
🇷🇼 flag rwanda rw flag nation country banner rwanda
🇸🇦 flag saudi arabia flag nation country banner saudi arabia
🇸🇧 flag solomon islands solomon islands flag nation country banner solomon islands
🇸🇨 flag seychelles sc flag nation country banner seychelles
🇸🇩 flag sudan sd flag nation country banner sudan
🇸🇪 flag sweden se flag nation country banner sweden
🇸🇬 flag singapore sg flag nation country banner singapore
🇸🇭 flag st helena saint helena ascension tristan cunha flag nation country banner st helena
🇸🇮 flag slovenia si flag nation country banner slovenia
🇸🇯 flag svalbard jan mayen
🇸🇰 flag slovakia sk flag nation country banner slovakia
🇸🇱 flag sierra leone sierra leone flag nation country banner sierra leone
🇸🇲 flag san marino san marino flag nation country banner san marino
🇸🇳 flag senegal sn flag nation country banner senegal
🇸🇴 flag somalia so flag nation country banner somalia
🇸🇷 flag suriname sr flag nation country banner suriname
🇸🇸 flag south sudan south sd flag nation country banner south sudan
🇸🇹 flag sao tome principe sao tome principe flag nation country banner sao tome principe
🇸🇻 flag el salvador el salvador flag nation country banner el salvador
🇸🇽 flag sint maarten sint maarten dutch flag nation country banner sint maarten
🇸🇾 flag syria syrian arab republic flag nation country banner syria
🇸🇿 flag eswatini sz flag nation country banner eswatini
🇹🇦 flag tristan da cunha
🇹🇨 flag turks caicos islands turks caicos islands flag nation country banner turks caicos islands
🇹🇩 flag chad td flag nation country banner chad
🇹🇫 flag french southern territories french southern territories flag nation country banner french southern territories
🇹🇬 flag togo tg flag nation country banner togo
🇹🇭 flag thailand th flag nation country banner thailand
🇹🇯 flag tajikistan tj flag nation country banner tajikistan
🇹🇰 flag tokelau tk flag nation country banner tokelau
🇹🇱 flag timor leste timor leste flag nation country banner timor leste
🇹🇲 flag turkmenistan flag nation country banner turkmenistan
🇹🇳 flag tunisia tn flag nation country banner tunisia
🇹🇴 flag tonga to flag nation country banner tonga
🇹🇷 flag turkey turkey flag nation country banner turkey
🇹🇹 flag trinidad tobago trinidad tobago flag nation country banner trinidad tobago
🇹🇻 flag tuvalu flag nation country banner tuvalu
🇹🇼 flag taiwan tw flag nation country banner taiwan
🇹🇿 flag tanzania tanzania united republic flag nation country banner tanzania
🇺🇦 flag ukraine ua flag nation country banner ukraine
🇺🇬 flag uganda ug flag nation country banner uganda
🇺🇲 flag u s outlying islands
🇺🇳 flag united nations un flag banner
🇺🇸 flag united states united states america flag nation country banner united states
🇺🇾 flag uruguay uy flag nation country banner uruguay
🇺🇿 flag uzbekistan uz flag nation country banner uzbekistan
🇻🇦 flag vatican city vatican city flag nation country banner vatican city
🇻🇨 flag st vincent grenadines saint vincent grenadines flag nation country banner st vincent grenadines
🇻🇪 flag venezuela ve bolivarian republic flag nation country banner venezuela
🇻🇬 flag british virgin islands british virgin islands bvi flag nation country banner british virgin islands
🇻🇮 flag u s virgin islands virgin islands us flag nation country banner u s virgin islands
🇻🇳 flag vietnam viet nam flag nation country banner vietnam
🇻🇺 flag vanuatu vu flag nation country banner vanuatu
🇼🇫 flag wallis futuna wallis futuna flag nation country banner wallis futuna
🇼🇸 flag samoa ws flag nation country banner samoa
🇽🇰 flag kosovo xk flag nation country banner kosovo
🇾🇪 flag yemen ye flag nation country banner yemen
🇾🇹 flag mayotte yt flag nation country banner mayotte
🇿🇦 flag south africa south africa flag nation country banner south africa
🇿🇲 flag zambia zm flag nation country banner zambia
🇿🇼 flag zimbabwe zw flag nation country banner zimbabwe
🏴󠁧󠁢󠁥󠁮󠁧󠁿 flag england flag english
🏴󠁧󠁢󠁳󠁣󠁴󠁿 flag scotland flag scottish
🏴󠁧󠁢󠁷󠁬󠁳󠁿 flag wales flag welsh
🥲 smiling face with tear sad cry pretend
🥸 disguised face pretent brows glasses moustache
🤌 pinched fingers size tiny small
🫀 anatomical heart health heartbeat
🫁 lungs breathe
🥷 ninja ninjutsu skills japanese
🤵‍♂️ man in tuxedo formal fashion
🤵‍♀️ woman in tuxedo formal fashion
👰‍♂️ man with veil wedding marriage
👰‍♀️ woman with veil wedding marriage
👩‍🍼 woman feeding baby birth food
👨‍🍼 man feeding baby birth food
🧑‍🍼 person feeding baby birth food
🧑‍🎄 mx claus christmas
🫂 people hugging care
🐈‍⬛ black cat superstition luck
🦬 bison ox
🦣 mammoth elephant tusks
🦫 beaver animal rodent
🐻‍❄️ polar bear animal arctic
🦤 dodo animal bird
🪶 feather bird fly
🦭 seal animal creature sea
🪲 beetle insect
🪳 cockroach insect pests
🪰 fly insect
🪱 worm animal
🪴 potted plant greenery house
🫐 blueberries fruit
🫒 olive fruit
🫑 bell pepper fruit plant
🫓 flatbread flour food
🫔 tamale food masa
🫕 fondue cheese pot food
🫖 teapot drink hot
🧋 bubble tea taiwan boba milk tea straw
🪨 rock stone
🪵 wood nature timber trunk
🛖 hut house structure
🛻 pickup truck car transportation
🛼 roller skate footwear sports
🪄 magic wand supernature power
🪅 pinata mexico candy celebration
🪆 nesting dolls matryoshka toy
🪡 sewing needle stitches
🪢 knot rope scout
🩴 thong sandal footwear summer
🪖 military helmet army protection
🪗 accordion music
🪘 long drum music
🪙 coin money currency
🪃 boomerang weapon
🪚 carpentry saw cut chop
🪛 screwdriver tools
🪝 hook tools
🪜 ladder tools
🛗 elevator lift
🪞 mirror reflection
🪟 window scenery
🪠 plunger toilet
🪤 mouse trap cheese
🪣 bucket water container
🪥 toothbrush hygiene dental
🪦 headstone death rip grave
🪧 placard announcement
⚧️ transgender symbol lgbtq
🏳️‍⚧️ transgender flag lgbtq
😶‍🌫️ face in clouds shower steam dream
😮‍💨 face exhaling relieve relief tired sigh
😵‍💫 face with spiral eyes sick ill confused nauseous nausea
❤️‍🔥 heart on fire passionate enthusiastic
❤️‍🩹 mending heart broken heart bandage wounded
🧔‍♂️ man beard facial hair
🧔‍♀️ woman beard facial hair
🫠 melting face hot heat
🫢 face with open eyes and hand over mouth silence secret shock surprise
🫣 face with peeking eye scared frightening embarrassing
🫡 saluting face respect salute
🫥 dotted line face invisible lonely isolation depression
🫤 face with diagonal mouth skeptic confuse frustrated indifferent
🥹 face holding back tears touched gratitude
🫱 rightwards hand palm offer
🫲 leftwards hand palm offer
🫳 palm down hand palm drop
🫴 palm up hand lift offer demand
🫰 hand with index finger and thumb crossed heart love money expensive
🫵 index pointing at the viewer you recruit
🫶 heart hands love appreciation support
🫦 biting lip flirt sexy pain worry
🫅 person with crown royalty power
🫃 pregnant man baby belly
🫄 pregnant person baby belly
🧌 troll mystical monster
🪸 coral ocean sea reef
🪷 lotus flower calm meditation
🪹 empty nest bird
🪺 nest with eggs bird
🫘 beans food
🫗 pouring liquid cup water
🫙 jar container sauce
🛝 playground slide fun park
🛞 wheel car transport
🛟 ring buoy life saver life preserver
🪬 hamsa religion protection
🪩 mirror ball disco dance party
🪫 low battery drained dead
🩼 crutch accessibility assist
🩻 x-ray skeleton medicine
🫧 bubbles soap fun carbonation sparkling
🪪 identification card document
🟰 heavy equals sign math
( ͡° ͜ʖ ͡°) lenny face that face
Α greek capital letter alpha alpha uppercase
α \alpha alpha greek small letter alpha lowercase
Β greek capital letter beta beta uppercase
β \beta beta greek small letter beta lowercase
Γ \Gamma Gamma greek capital letter gamma uppercase
γ \gamma gamma greek small letter gamma lowercase
Δ \Delta Delta greek capital letter delta uppercase
δ \delta delta greek small letter delta lowercase
Ε greek capital letter epsilon epsilon uppercase
ε \epsilon epsilon greek small letter epsilon lowercase
Ζ greek capital letter zeta zeta uppercase
ζ \zeta zeta greek small letter zeta lowercase
Η greek capital letter eta eta uppercase
η \eta eta greek small letter eta lowercase
Θ \Theta Theta greek capital letter theta uppercase
θ \theta theta greek small letter theta lowercase
Ι greek capital letter iota iota uppercase
ι \iota iota greek small letter iota lowercase
Κ greek capital letter kappa kappa uppercase
κ \kappa kappa greek small letter kappa lowercase
Λ \Lambda Lambda greek capital letter lambda uppercase
λ \lambda lambda greek small letter lambda lowercase
Μ greek capital letter mu mu uppercase
μ \mu mu greek small letter mu lowercase
Ν greek capital letter nu nu uppercase
ν \nu nu greek small letter nu lowercase
Ξ \Xi Xi greek capital letter xi uppercase
ξ \xi xi greek small letter xi lowercase
Ο greek capital letter omicron omicron uppercase
ο greek small letter omicron omicron lowercase
Π \Pi Pi greek capital letter pi uppercase
π \pi pi greek small letter pi lowercase
Ρ greek capital letter rho rho uppercase
ρ \rho rho greek small letter rho lowercase
Σ \Sigma Sigma greek capital letter sigma uppercase
σ \sigma sigma greek small letter sigma lowercase
ς \varsigma varsigma greek small letter final sigma final sigma lowercase var sigma
Τ greek capital letter tau tau uppercase
τ \tau tau greek small letter tau lowercase
Υ \Upsilon Upsilon greek capital letter upsilon uppercase
υ \upsilon upsilon greek small letter upsilon lowercase
Φ \Phi Phi greek capital letter phi uppercase
φ \phi phi greek small letter phi lowercase
Χ \Chi Chi greek capital letter chi uppercase
χ \chi chi greek small letter chi lowercase
Ψ \Psi Psi greek capital letter psi uppercase
ψ \psi psi greek small letter psi lowercase
Ω \Omega Omega greek capital letter omega uppercase
ω \omega omega greek small letter omega lowercase
ϵ \varepsilon varepsilon var epsilon greek lunate epsilon symbol
ϑ \vartheta vartheta var theta greek theta symbol
ϰ \varkappa varkappa var kappa greek kappa symbol
ϱ \varrho varrho var rho greek rho symbol
ϕ \varphi varphi var phi greek phi symbol
ϖ \varpi varpi var pi greek pi symbol
ℝ \mathbb{R} \Bbb{R} \bbR \RR reals real numbers blackboard doublestruck R
ℤ \mathbb{Z} \Bbb{Z} \bbZ \ZZ integers integer numbers blackboard doublestruck Z
ℕ \mathbb{N} \Bbb{N} \bbN \NN naturals natural numbers blackboard doublestruck N
ℚ \mathbb{Q} \Bbb{Q} \bbQ \QQ rationals rational numbers blackboard doublestruck Q
ℂ \mathbb{C} \Bbb{C} \bbC \CC complex complexes complex numbers blackboard doublestruck C
ℙ \mathbb{P} \Bbb{P} \bbP \PP probability primes powerset blackboard doublestruck P
ℍ \mathbb{H} \Bbb{H} \bbH \HH quaternions hamiltonians blackboard doublestruck H
× \times times multiply multiplication cross
· \cdot cdot centered dot multiplication
± \pm plusminus plus minus
≤ \le \leq le leq less or equal
≥ \ge \geq ge geq greater or equal
≠ \ne \neq not equals not equal
≈ \approx approximately approx
≡ \equiv equivalent equivalence identity
∞ \infty infinity
∂ \partial partial derivative
∇ \nabla nabla del gradient
∑ \sum sum summation
∏ \prod product
∫ \int integral
∈ \in element of in membership
∉ \notin notin not in
∅ \emptyset \varnothing empty set emptyset varnothing
⊂ \subset proper subset subset
⊆ \subseteq subseteq subset or equal
⊃ \supset proper superset superset
⊇ \supseteq superset or equal
∪ \cup union set union
∩ \cap intersection set intersection
⊥ \perp perpendicular orthogonal bot bottom false
∥ \parallel parallel
∘ \circ small circle function composition ring operator
° ^\circ degree degrees
→ \to \rightarrow right arrow arrow
← \leftarrow left arrow arrow
⇒ \Rightarrow implies implication right double arrow implies
⇐ \Leftarrow impliedby left double arrow impliedby
⇔ \Leftrightarrow iff equivalence double arrow iff
↔ \leftrightarrow left right arrow double arrow
↦ \mapsto mapsto maps to
∀ \forall for all universal quantifier
∃ \exists there exists existential quantifier
¬ \neg not logical not
∧ \land and logical and
∨ \lor or logical or
⟨ \langle langle left angle bracket
⟩ \rangle rangle right angle bracket
′ \prime prime derivative feet minutes
″ double prime dprime seconds inches
√ \sqrt square root radical
⊤ \top top true truth
⊢ \vdash turnstile entails provable proves entailment
⊣ \dashv dashv left turnstile
⊨ \models \vDash models semantic consequence entails
⊩ \Vdash forces forcing semantic entails
⊪ \Vvdash triple turnstile semantic entails
⊻ \veebar xor exclusive or
∖ \setminus setminus set difference
∴ \therefore therefore
∵ \because because
∋ \ni contains as member ni
∌ \not\ni not contains notni not member
∄ \nexists not exists there does not exist
⊄ \nsubset not subset
⊅ \nsupset not superset
⊈ \nsubseteq not subseteq not subset or equal
⊉ \nsupseteq not superset or equal
⊊ \subsetneq proper subset not equal subsetneq
⊋ \supsetneq proper superset not equal supsetneq
⊎ \uplus uplus disjoint union
⋂ \bigcap bigcap n-ary intersection
⋃ \bigcup bigcup n-ary union
⋁ \bigvee bigvee n-ary or
⋀ \bigwedge bigwedge n-ary and
⨆ \bigsqcup bigsqcup n-ary square union
⨄ \biguplus biguplus n-ary uplus disjoint union big
⊕ \oplus direct sum oplus circled plus
⊗ \otimes tensor product otimes circled times
⊖ \ominus ominus circled minus
⊘ \oslash oslash circled slash division
⊙ \odot odot circled dot
⨁ \bigoplus bigoplus n-ary circled plus direct sum
⨂ \bigotimes bigotimes n-ary circled times
⨀ \bigodot bigodot n-ary circled dot
⋮ \vdots vertical dots
⋱ \ddots diagonal dots down-right
⋯ \cdots centered dots midline ellipsis
… \ldots ldots horizontal ellipsis
∎ \qed QED end of proof tombstone
≅ \cong congruent isomorphic isomorphism cong
≇ \ncong not congruent not isomorphic ncong
≃ \simeq simeq asymptotically equal similar approx equal
∼ \sim sim similar tilde relation
≲ \lesssim lesssim less than or similar
≳ \gtrsim gtrsim greater than or similar
≶ \lessgtr lessgtr less greater
≷ \gtrless gtrless greater less
≼ \preceq preceq precedes or equal
≽ \succeq succeq succeeds or equal
≺ \prec prec precedes
≻ \succ succ succeeds
⊑ \sqsubseteq sqsubseteq square subset or equal
⊒ \sqsupseteq sqsupseteq square superset or equal
⊏ \sqsubset sqsubset square subset
⊐ \sqsupset sqsupset square superset
∝ \propto proportional propto proportional to
≍ \asymp asymp asymptotically equal
# ——— Arrows: basics, long, hooks, tails, harpoons, negated ———
↑ \uparrow up arrow
↓ \downarrow down arrow
↕ \updownarrow updown arrow
⇑ \Uparrow double up arrow
⇓ \Downarrow double down arrow
⇕ \Updownarrow double updown arrow
↗ \nearrow ne arrow
↘ \searrow se arrow
↙ \swarrow sw arrow
↖ \nwarrow nw arrow
⟶ \longrightarrow longrightarrow long right arrow
⟵ \longleftarrow longleftarrow long left arrow
⟷ \longleftrightarrow longleftrightarrow long left right arrow
⟹ \Longrightarrow Longrightarrow long double right arrow
⟸ \Longleftarrow Longleftarrow long double left arrow
⟺ \Longleftrightarrow Longleftrightarrow long double left right arrow
⟼ \longmapsto longmapsto long maps to
↦ \mapsto mapsto maps to
↤ \mapsfrom mapsfrom leftwards from bar
↣ \rightarrowtail rightarrowtail arrow with tail
↢ \leftarrowtail leftarrowtail arrow with tail
↪ \hookrightarrow hookrightarrow hook right arrow
↩ \hookleftarrow hookleftarrow hook left arrow
↠ \twoheadrightarrow twoheadrightarrow two headed right arrow
↞ \twoheadleftarrow twoheadleftarrow two headed left arrow
⇄ \rightleftarrows rightleftarrows right over left arrows
⇆ \leftrightarrows leftrightarrows left over right arrows
↼ \leftharpoonup leftharpoonup harpoon
↽ \leftharpoondown leftharpoondown harpoon
⇀ \rightharpoonup rightharpoonup harpoon
⇁ \rightharpoondown rightharpoondown harpoon
↾ \upharpoonright upharpoonright harpoon
↿ \upharpoonleft upharpoonleft harpoon
⇂ \downharpoonright downharpoonright harpoon
⇃ \downharpoonleft downharpoonleft harpoon
⇋ \leftrightharpoons leftrightharpoons
⇌ \rightleftharpoons rightleftharpoons
⇝ \leadsto leadsto right squiggle arrow
↚ \nleftarrow nleftarrow not left arrow
↛ \nrightarrow nrightarrow not right arrow
↮ \nleftrightarrow nleftrightarrow not left right arrow
⇍ \nLeftarrow nLeftarrow not Leftarrow
⇏ \nRightarrow nRightarrow not Rightarrow
⇎ \nLeftrightarrow nLeftrightarrow not Leftrightarrow

# ——— Relations: order/equality variants, divisibility, parallels ———
≪ \ll ll much less
≫ \gg gg much greater
≮ \nless nless not less than
≯ \ngtr ngtr not greater than
≰ \nleq nleq not less or equal
≱ \ngeq ngeq not greater or equal
≨ \lneqq lneqq less than but not equal
≩ \gneqq gneqq greater than but not equal
≢ \nequiv nequiv not equivalent
∣ \mid mid divides such that
∤ \nmid nmid not divides
∥ \parallel parallel
∦ \nparallel nparallel not parallel

# ——— Geometry and delimiters ———
∠ \angle angle
∡ \measuredangle measuredangle
∢ \sphericalangle sphericalangle
⌈ \lceil lceil left ceiling
⌉ \rceil rceil right ceiling
⌊ \lfloor lfloor left floor
⌋ \rfloor rfloor right floor
⟦ \llbracket llbracket left double bracket
⟧ \rrbracket rrbracket right double bracket

# ——— Arithmetic/definitions ———
÷ \div division obelus
∓ \mp minusplus
≐ \doteq doteq
≑ \doteqdot doteqdot
≔ \coloneqq coloneqq definition equals
≕ \eqqcolon eqqcolon equals colon
≜ \triangleq triangleq definition equal triangle
⏦ \accurrent accurrent ac current
♾ \acidfree acidfree permanent paper sign
́ \acute acute acute accent
⥀ \acwcirclearrow acwcirclearrow anticlockwise closed circle arrow
⟲ \acwgapcirclearrow acwgapcirclearrow anticlockwise gapped circle arrow
⤹ \acwleftarcarrow acwleftarcarrow left-side arc anticlockwise arrow
↺ \acwopencirclearrow acwopencirclearrow anticlockwise open circle arrow
⤺ \acwoverarcarrow acwoverarcarrow top arc anticlockwise arrow
⤻ \acwunderarcarrow acwunderarcarrow bottom arc anticlockwise arrow
⋰ \adots adots three dots, ascending
ℵ \aleph aleph aleph, hebrew
⨿ \amalg amalg amalgamation or coproduct
⦟ \angdnr angdnr acute angle
∠ \angle angle angle
⦞ \angles angles angle with s inside
⦤ \angleubar angleubar angle with underbar
Å \Angstrom Angstrom angstrom capital a, ring
⃧ \annuity annuity combining annuity symbol
⍰ \APLboxquestion APLboxquestion boxed question mark
⍓ \APLboxupcaret APLboxupcaret boxed up caret
⍀ \APLnotbackslash APLnotbackslash apl functional symbol backslash bar
⌿ \APLnotslash APLnotslash solidus, bar through (apl functional symbol slash bar)
≈ \approx approx approximate
≊ \approxeq approxeq approximate, equals
⩰ \approxeqq approxeqq approximately equal or equal to
≋ \approxident approxident approximately identical to
𞻱 \arabichad arabichad arabic mathematical operator hah with dal
𞻰 \arabicmaj arabicmaj arabic mathematical operator meem with hah with tatweel
≘ \arceq arceq arc, equals; corresponds to
⊦ \assert assert assertion (vertical, short dash)
∗ \ast ast centered asterisk
⩮ \asteq asteq equals with asterisk
⃰ \asteraccent asteraccent combining asterisk above
☉ \astrosun astrosun sun
≍ \asymp asymp asymptotically equal to
⨑ \awint awint anticlockwise integration
≌ \backcong backcong all equal to
‶ \backdprime backdprime double reverse prime, not superscripted
‵ \backprime backprime reverse prime, not superscripted
∽ \backsim backsim reverse similar
⋍ \backsimeq backsimeq reverse similar, equals
\ \backslash backslash reverse solidus
‷ \backtrprime backtrprime triple reverse prime, not superscripted
⋿ \bagmember bagmember z notation bag membership
̄ \bar bar macron
⩃ \barcap barcap intersection with overbar
⩂ \barcup barcup union with overbar
⥡ \bardownharpoonleft bardownharpoonleft downwards harpoon with barb left from bar
⥝ \bardownharpoonright bardownharpoonright downwards harpoon with barb right from bar
⇤ \barleftarrow barleftarrow leftwards arrow to bar
↹ \barleftarrowrightarrowbar barleftarrowrightarrowbar leftwards arrow to bar over rightwards arrow to bar
⥖ \barleftharpoondown barleftharpoondown leftwards harpoon with barb down to bar
⥒ \barleftharpoonup barleftharpoonup leftwards harpoon with barb up to bar
↸ \barovernorthwestarrow barovernorthwestarrow north west arrow to long bar
⤠ \barrightarrowdiamond barrightarrowdiamond rightwards arrow from bar to black diamond
⥟ \barrightharpoondown barrightharpoondown rightwards harpoon with barb down from bar
⥛ \barrightharpoonup barrightharpoonup rightwards harpoon with barb up from bar
⤒ \baruparrow baruparrow upwards arrow to bar
⥘ \barupharpoonleft barupharpoonleft upwards harpoon with barb left to bar
⥔ \barupharpoonright barupharpoonright upwards harpoon with barb right to bar
⫪ \barV barV double down tack
⫧ \Barv Barv short down tack with overbar
⊽ \barvee barvee bar, vee (large vee)
⊼ \barwedge barwedge bar, wedge (large wedge)
𝕒 \Bbba Bbba mathematical double-struck small a
𝔸 \BbbA BbbA mathematical double-struck capital a
𝕓 \Bbbb Bbbb mathematical double-struck small b
𝔹 \BbbB BbbB mathematical double-struck capital b
𝕔 \Bbbc Bbbc mathematical double-struck small c
ℂ \BbbC BbbC /bbb c, open face c
𝕕 \Bbbd Bbbd mathematical double-struck small d
𝔻 \BbbD BbbD mathematical double-struck capital d
𝕖 \Bbbe Bbbe mathematical double-struck small e
𝔼 \BbbE BbbE mathematical double-struck capital e
𝟠 \Bbbeight Bbbeight mathematical double-struck digit 8
𝕗 \Bbbf Bbbf mathematical double-struck small f
𝔽 \BbbF BbbF mathematical double-struck capital f
𝟝 \Bbbfive Bbbfive mathematical double-struck digit 5
𝟜 \Bbbfour Bbbfour mathematical double-struck digit 4
𝕘 \Bbbg Bbbg mathematical double-struck small g
𝔾 \BbbG BbbG mathematical double-struck capital g
ℽ \Bbbgamma Bbbgamma double-struck small gamma
ℾ \BbbGamma BbbGamma double-struck capital gamma
𝕙 \Bbbh Bbbh mathematical double-struck small h
ℍ \BbbH BbbH /bbb h, open face h
𝕚 \Bbbi Bbbi mathematical double-struck small i
𝕀 \BbbI BbbI mathematical double-struck capital i
𝕛 \Bbbj Bbbj mathematical double-struck small j
𝕁 \BbbJ BbbJ mathematical double-struck capital j
𝕜 \Bbbk Bbbk mathematical double-struck small k
𝕂 \BbbK BbbK mathematical double-struck capital k
𝕝 \Bbbl Bbbl mathematical double-struck small l
𝕃 \BbbL BbbL mathematical double-struck capital l
𝕞 \Bbbm Bbbm mathematical double-struck small m
𝕄 \BbbM BbbM mathematical double-struck capital m
𝕟 \Bbbn Bbbn mathematical double-struck small n
ℕ \BbbN BbbN /bbb n, open face n
𝟡 \Bbbnine Bbbnine mathematical double-struck digit 9
𝕠 \Bbbo Bbbo mathematical double-struck small o
𝕆 \BbbO BbbO mathematical double-struck capital o
𝟙 \Bbbone Bbbone mathematical double-struck digit 1
𝕡 \Bbbp Bbbp mathematical double-struck small p
ℙ \BbbP BbbP /bbb p, open face p
ℼ \Bbbpi Bbbpi double-struck small pi
ℿ \BbbPi BbbPi double-struck capital pi
𝕢 \Bbbq Bbbq mathematical double-struck small q
ℚ \BbbQ BbbQ /bbb q, open face q
𝕣 \Bbbr Bbbr mathematical double-struck small r
ℝ \BbbR BbbR /bbb r, open face r
𝕤 \Bbbs Bbbs mathematical double-struck small s
𝕊 \BbbS BbbS mathematical double-struck capital s
𝟟 \Bbbseven Bbbseven mathematical double-struck digit 7
𝟞 \Bbbsix Bbbsix mathematical double-struck digit 6
⅀ \Bbbsum Bbbsum double-struck n-ary summation
𝕥 \Bbbt Bbbt mathematical double-struck small t
𝕋 \BbbT BbbT mathematical double-struck capital t
𝟛 \Bbbthree Bbbthree mathematical double-struck digit 3
𝟚 \Bbbtwo Bbbtwo mathematical double-struck digit 2
𝕦 \Bbbu Bbbu mathematical double-struck small u
𝕌 \BbbU BbbU mathematical double-struck capital u
𝕧 \Bbbv Bbbv mathematical double-struck small v
𝕍 \BbbV BbbV mathematical double-struck capital v
𝕨 \Bbbw Bbbw mathematical double-struck small w
𝕎 \BbbW BbbW mathematical double-struck capital w
𝕩 \Bbbx Bbbx mathematical double-struck small x
𝕏 \BbbX BbbX mathematical double-struck capital x
𝕪 \Bbby Bbby mathematical double-struck small y
𝕐 \BbbY BbbY mathematical double-struck capital y
𝕫 \Bbbz Bbbz mathematical double-struck small z
ℤ \BbbZ BbbZ /bbb z, open face z
𝟘 \Bbbzero Bbbzero mathematical double-struck digit 0
⎶ \bbrktbrk bbrktbrk bottom square bracket over top square bracket
┆ \bdtriplevdash bdtriplevdash doubly broken vert
∵ \because because because
⏣ \benzenr benzenr benzene ring with circle
ℶ \beth beth beth, hebrew
≬ \between between between
▼ \bigblacktriangledown bigblacktriangledown big down triangle, filled
▲ \bigblacktriangleup bigblacktriangleup black up-pointing triangle
⟘ \bigbot bigbot large up tack
⋂ \bigcap bigcap intersection operator
⋃ \bigcup bigcup union operator
⨃ \bigcupdot bigcupdot n-ary union operator with dot
⫼ \biginterleave biginterleave large triple vertical bar operator
⨀ \bigodot bigodot n-ary circled dot operator
⨁ \bigoplus bigoplus n-ary circled plus operator
⨂ \bigotimes bigotimes n-ary circled times operator
⩗ \bigslopedvee bigslopedvee sloping large or
⩘ \bigslopedwedge bigslopedwedge sloping large and
⨅ \bigsqcap bigsqcap n-ary square product (big sqcap)
⨆ \bigsqcup bigsqcup n-ary square union operator
★ \bigstar bigstar star, filled
⫿ \bigtalloblong bigtalloblong n-ary white vertical bar
⨉ \bigtimes bigtimes n-ary times operator
⟙ \bigtop bigtop large down tack
▽ \bigtriangledown bigtriangledown big down triangle, open
⨞ \bigtriangleleft bigtriangleleft large left triangle operator
△ \bigtriangleup bigtriangleup big up triangle, open
⨄ \biguplus biguplus n-ary union operator with plus
⋁ \bigvee bigvee logical or operator
⋀ \bigwedge bigwedge logical and operator
☆ \bigwhitestar bigwhitestar star, open
⧭ \blackcircledownarrow blackcircledownarrow black circle with down arrow
⚈ \blackcircledrightdot blackcircledrightdot black circle with white dot right
⚉ \blackcircledtwodots blackcircledtwodots black circle with two white dots
◕ \blackcircleulquadwhite blackcircleulquadwhite circle with all but upper left quadrant black
⧪ \blackdiamonddownarrow blackdiamonddownarrow black diamond with down arrow
⧗ \blackhourglass blackhourglass black hourglass
◈ \blackinwhitediamond blackinwhitediamond white diamond containing black small diamond
▣ \blackinwhitesquare blackinwhitesquare white square containing black small square
◖ \blacklefthalfcircle blacklefthalfcircle left half black circle
◄ \blackpointerleft blackpointerleft black left-pointing pointer
► \blackpointerright blackpointerright black right-pointing pointer
◗ \blackrighthalfcircle blackrighthalfcircle right half black circle
☻ \blacksmiley blacksmiley black smiling face
▴ \blacktriangle blacktriangle up triangle, filled
▾ \blacktriangledown blacktriangledown down triangle, filled
◀ \blacktriangleleft blacktriangleleft (large) left triangle, filled
▶ \blacktriangleright blacktriangleright (large) right triangle, filled
␢ \blanksymbol blanksymbol blank symbol
⬬ \blkhorzoval blkhorzoval black horizontal ellipse
⬮ \blkvertoval blkvertoval black vertical ellipse
█ \blockfull blockfull full block
▒ \blockhalfshaded blockhalfshaded 50\% shaded block
▌ \blocklefthalf blocklefthalf left half block
▄ \blocklowhalf blocklowhalf lower half block
░ \blockqtrshaded blockqtrshaded 25\% shaded block
▐ \blockrighthalf blockrighthalf right half block
▓ \blockthreeqtrshaded blockthreeqtrshaded 75\% shaded block
▀ \blockuphalf blockuphalf upper half block
⫭ \bNot bNot reversed double stroke not sign
⊥ \bot bot bottom
◡ \botsemicircle botsemicircle lower half circle
⋈ \bowtie bowtie bowtie
⧆ \boxast boxast squared asterisk
◫ \boxbar boxbar vertical bar in box
⧈ \boxbox boxbox squared square
⧅ \boxbslash boxbslash squared falling diagonal slash
⧇ \boxcircle boxcircle squared small circle
⧄ \boxdiag boxdiag squared rising diagonal slash
⊡ \boxdot boxdot /dotsquare /boxdot b: small dot in box
⊟ \boxminus boxminus minus sign in box
⧉ \boxonbox boxonbox two joined squares
⊞ \boxplus boxplus plus sign in box
⊠ \boxtimes boxtimes multiply sign in box
̆ \breve breve breve
⭁ \bsimilarleftarrow bsimilarleftarrow reverse tilde operator above leftwards arrow
⭇ \bsimilarrightarrow bsimilarrightarrow reverse tilde operator above rightwards arrow
⟈ \bsolhsub bsolhsub reverse solidus preceding subset
⨲ \btimes btimes semidirect product with bottom closed
◎ \bullseye bullseye bullseye
≏ \bumpeq bumpeq bumpy equals, equals
≎ \Bumpeq Bumpeq bumpy equals
⪮ \bumpeqq bumpeqq equals sign with bumpy above
̐ \candra candra candrabindu (non-spacing)
∩ \cap cap intersection
⋒ \Cap Cap /cap /doublecap b: double intersection
⩉ \capbarcup capbarcup intersection above bar above union
⩀ \capdot capdot intersection with dot
⩇ \capovercup capovercup intersection above union
⩄ \capwedge capwedge intersection with logical and
‸ \caretinsert caretinsert caret (insertion mark)
↵ \carriagereturn carriagereturn downwards arrow with corner leftward = carriage return
⤿ \ccwundercurvearrow ccwundercurvearrow lower left semicircular anticlockwise arrow
⋅ \cdot cdot small middle dot
· \cdotp cdotp /centerdot b: middle dot
̌ \check check caron
✓ \checkmark checkmark tick, check mark
⟟ \cirbot cirbot up tack with circle above
≗ \circeq circeq circle, equals
◒ \circlebottomhalfblack circlebottomhalfblack circle, filled bottom half
⊛ \circledast circledast asterisk in circle
⦿ \circledbullet circledbullet circled bullet
⊚ \circledcirc circledcirc small circle in circle
⊝ \circleddash circleddash hyphen in circle
⊜ \circledequal circledequal equal in circle
⧬ \circledownarrow circledownarrow white circle with down arrow
⦷ \circledparallel circledparallel circled parallel
⚆ \circledrightdot circledrightdot white circle with dot right
✪ \circledstar circledstar circled white star
⚇ \circledtwodots circledtwodots white circle with two dots
⦶ \circledvert circledvert circled vertical bar
⦾ \circledwhitebullet circledwhitebullet circled white bullet
⦵ \circlehbar circlehbar circle with horizontal bar
◐ \circlelefthalfblack circlelefthalfblack circle, filled left half [harvey ball]
◵ \circlellquad circlellquad white circle with lower left quadrant
◶ \circlelrquad circlelrquad white circle with lower right quadrant
⬰ \circleonleftarrow circleonleftarrow left arrow with small circle
⇴ \circleonrightarrow circleonrightarrow right arrow with small circle
◑ \circlerighthalfblack circlerighthalfblack circle, filled right half
◓ \circletophalfblack circletophalfblack circle, filled top half
◴ \circleulquad circleulquad white circle with upper left quadrant
◷ \circleurquad circleurquad white circle with upper right quadrant
◔ \circleurquadblack circleurquadblack circle with upper right quadrant black
◍ \circlevertfill circlevertfill circle with vertical fill
⧃ \cirE cirE circle with two horizontal strokes to the right
⨐ \cirfnint cirfnint circulation function
⫯ \cirmid cirmid vertical line with circle above
⧂ \cirscir cirscir circle with small circle to the right
⩍ \closedvarcap closedvarcap closed intersection with serifs
⩌ \closedvarcup closedvarcup closed union with serifs
⩐ \closedvarcupsmashprod closedvarcupsmashprod closed union with serifs and smash product
⁐ \closure closure close up
♣ \clubsuit clubsuit club suit symbol
∷ \Colon Colon two colons
≔ \coloneq coloneq colon, equals
⩴ \Coloneq Coloneq double colon equal
⨩ \commaminus commaminus minus sign with comma above
∁ \complement complement complement sign
⟡ \concavediamond concavediamond white concave-sided diamond
⟢ \concavediamondtickleft concavediamondtickleft white concave-sided diamond with leftwards tick
⟣ \concavediamondtickright concavediamondtickright white concave-sided diamond with rightwards tick
≅ \cong cong congruent with
⩭ \congdot congdot congruent with dot above
⌲ \conictaper conictaper conical taper
⨇ \conjquant conjquant two logical and operator
∐ \coprod coprod coproduct operator
⫏ \csub csub closed subset
⫑ \csube csube closed subset or equal to
⫐ \csup csup closed superset
⫒ \csupe csupe closed superset or equal to
∛ \cuberoot cuberoot cube root
∪ \cup cup union or logical sum
⋓ \Cup Cup /cup /doublecup b: double union
⩈ \cupbarcap cupbarcap union above bar above intersection
⊍ \cupdot cupdot union, with dot
⊌ \cupleftarrow cupleftarrow multiset
⩆ \cupovercap cupovercap union above intersection
⩅ \cupvee cupvee union with logical or
⋞ \curlyeqprec curlyeqprec curly equals, precedes
⋟ \curlyeqsucc curlyeqsucc curly equals, succeeds
⋎ \curlyvee curlyvee curly logical or
⋏ \curlywedge curlywedge curly logical and
↶ \curvearrowleft curvearrowleft left curved arrow
⤽ \curvearrowleftplus curvearrowleftplus top arc anticlockwise arrow with plus
↷ \curvearrowright curvearrowright right curved arrow
⤼ \curvearrowrightminus curvearrowrightminus top arc clockwise arrow with minus
⥁ \cwcirclearrow cwcirclearrow clockwise closed circle arrow
⟳ \cwgapcirclearrow cwgapcirclearrow clockwise gapped circle arrow
↻ \cwopencirclearrow cwopencirclearrow clockwise open circle arrow
⤸ \cwrightarcarrow cwrightarcarrow right-side arc clockwise arrow
⤾ \cwundercurvearrow cwundercurvearrow lower right semicircular clockwise arrow
† \dagger dagger dagger relation
ℸ \daleth daleth daleth, hebrew
☡ \danger danger dangerous bend (caution sign)
∹ \dashcolon dashcolon excess (-:)
⥫ \dashleftharpoondown dashleftharpoondown leftwards harpoon with barb down below long dash
⥭ \dashrightharpoondown dashrightharpoondown rightwards harpoon with barb down below long dash
⊣ \dashv dashv dash, vertical
⫣ \dashV dashV double vertical bar left turnstile
⫤ \Dashv Dashv vertical bar double left turnstile
⫥ \DashV DashV double vertical bar double left turnstile
⟛ \dashVdash dashVdash left and right tack
⟚ \DashVDash DashVDash left and right double turnstile
⤏ \dbkarrow dbkarrow rightwards triple dash arrow
‡ \ddagger ddagger double dagger relation
⃜ \ddddot ddddot combining four dots above
⃛ \dddot dddot combining three dots above
̈ \ddot ddot dieresis
⋱ \ddots ddots three dots, descending
⩷ \ddotseq ddotseq equals sign with two dots above and two dots below
⤋ \Ddownarrow Ddownarrow downwards triple arrow
⟱ \DDownarrow DDownarrow downwards quadruple arrow
⟍ \diagdown diagdown mathematical falling diagonal
⟋ \diagup diagup mathematical rising diagonal
⌀ \diameter diameter diameter sign
⬙ \diamondbotblack diamondbotblack diamond with bottom half black
⟐ \diamondcdot diamondcdot white diamond with centred dot
⤝ \diamondleftarrow diamondleftarrow leftwards arrow to black diamond
⤟ \diamondleftarrowbar diamondleftarrowbar leftwards arrow from bar to black diamond
⬖ \diamondleftblack diamondleftblack diamond with left half black
⬗ \diamondrightblack diamondrightblack diamond with right half black
♢ \diamondsuit diamondsuit diamond suit symbol
⬘ \diamondtopblack diamondtopblack diamond with top half black
⚀ \dicei dicei die face-1
⚁ \diceii diceii die face-2
⚂ \diceiii diceiii die face-3
⚃ \diceiv diceiv die face-4
⚄ \dicev dicev die face-5
⚅ \dicevi dicevi die face-6
✽ \dingasterisk dingasterisk heavy teardrop-spoked asterisk
⋲ \disin disin element of with long horizontal stroke
⨈ \disjquant disjquant two logical or operator
÷ \div div divide sign
⋇ \divideontimes divideontimes division on times
∕ \divslash divslash division slash
̇ \dot dot dot above
≐ \doteq doteq equals, single dot above
≑ \Doteq Doteq /doteqdot /doteq r: equals, even dots
⩧ \dotequiv dotequiv identical with dot above
∸ \dotminus dotminus minus sign, dot above
∔ \dotplus dotplus plus sign, dot above
⩪ \dotsim dotsim tilde operator with dot above
∺ \dotsminusdots dotsminusdots minus with four dots, geometric properties
◌ \dottedcircle dottedcircle dotted circle
⬚ \dottedsquare dottedsquare dotted square
⨰ \dottimes dottimes multiplication sign with dot above
⩢ \doublebarvee doublebarvee logical or with double overbar
⩞ \doublebarwedge doublebarwedge logical and with double overbar
⧺ \doubleplus doubleplus double plus
↓ \downarrow downarrow downward arrow
⇓ \Downarrow Downarrow down double arrow
⤓ \downarrowbar downarrowbar downwards arrow to bar
⤈ \downarrowbarred downarrowbarred downwards arrow with horizontal stroke
⇣ \downdasharrow downdasharrow downwards dashed arrow
⇊ \downdownarrows downdownarrows two down arrows
⥿ \downfishtail downfishtail down fish tail
⇃ \downharpoonleft downharpoonleft down harpoon-left
⥙ \downharpoonleftbar downharpoonleftbar downwards harpoon with barb left to bar
⇂ \downharpoonright downharpoonright down harpoon-right
⥕ \downharpoonrightbar downharpoonrightbar downwards harpoon with barb right to bar
⥥ \downharpoonsleftright downharpoonsleftright downwards harpoon with barb left beside downwards harpoon with barb right
⤵ \downrightcurvedarrow downrightcurvedarrow arrow pointing rightwards then curving downwards
⧨ \downtriangleleftblack downtriangleleftblack down-pointing triangle with left half black
⧩ \downtrianglerightblack downtrianglerightblack down-pointing triangle with right half black
⇵ \downuparrows downuparrows downwards arrow leftwards of upwards arrow
⥯ \downupharpoonsleftright downupharpoonsleftright downwards harpoon with barb left beside upwards harpoon with barb right
⇩ \downwhitearrow downwhitearrow downwards white arrow
↯ \downzigzagarrow downzigzagarrow downwards zigzag arrow
″ \dprime dprime double prime or second, not superscripted
➛ \draftingarrow draftingarrow right arrow with bold head (drafting)
⤐ \drbkarrow drbkarrow rightwards two-headed triple dash arrow
̚ \droang droang left angle above (non-spacing)
⧶ \dsol dsol solidus with overbar
⩤ \dsub dsub z notation domain antirestriction
⧟ \dualmap dualmap double-ended multimap
⪘ \egsdot egsdot slanted equal to or greater-than with dot inside
♪ \eighthnote eighthnote eighth note
⏧ \elinters elinters electrical intersection
ℓ \ell ell cursive small l
⪗ \elsdot elsdot slanted equal to or less-than with dot inside
⦳ \emptysetoarr emptysetoarr empty set with right arrow above
⦴ \emptysetoarrl emptysetoarrl empty set with left arrow above
⦱ \emptysetobar emptysetobar empty set with overbar
⦲ \emptysetocirc emptysetocirc empty set with small circle above
⃝ \enclosecircle enclosecircle combining enclosing circle
⃟ \enclosediamond enclosediamond combining enclosing diamond
⃞ \enclosesquare enclosesquare combining enclosing square
⃤ \enclosetriangle enclosetriangle combining enclosing upward pointing triangle
‥ \enleadertwodots enleadertwodots double baseline dot (en leader)
⧣ \eparsl eparsl equals sign and slanted parallel
≖ \eqcirc eqcirc circle on equals sign
≕ \eqcolon eqcolon equals, colon
≝ \eqdef eqdef equals by definition
⩦ \eqdot eqdot equals sign with dot below
⩵ \eqeq eqeq two consecutive equals signs
⩶ \eqeqeq eqeqeq three consecutive equals signs
⋝ \eqgtr eqgtr equal-or-greater
⋜ \eqless eqless equal-or-less
⪚ \eqqgtr eqqgtr double-line equal to or greater-than
⪙ \eqqless eqqless double-line equal to or less-than
⩱ \eqqplus eqqplus equals sign above plus sign
⩳ \eqqsim eqqsim equals sign above tilde operator
⪜ \eqqslantgtr eqqslantgtr double-line slanted equal to or greater-than
⪛ \eqqslantless eqqslantless double-line slanted equal to or less-than
≂ \eqsim eqsim equals, similar
⪖ \eqslantgtr eqslantgtr slanted equal to or greater-than
⪕ \eqslantless eqslantless slanted equal to or less-than
= \equal equal equals sign r:
⭀ \equalleftarrow equalleftarrow equals sign above leftwards arrow
⋕ \equalparallel equalparallel parallel, equal; equal or parallel
⥱ \equalrightarrow equalrightarrow equals sign above rightwards arrow
≡ \equiv equiv identical with
≣ \Equiv Equiv strict equivalence (4 lines)
⩸ \equivDD equivDD equivalent with four dots above
⩨ \equivVert equivVert triple horizontal bar with double vertical stroke
⩩ \equivVvert equivVvert triple horizontal bar with triple vertical stroke
⧥ \eqvparsl eqvparsl identical to and slanted parallel
⧳ \errbarblackcircle errbarblackcircle error-barred black circle
⧱ \errbarblackdiamond errbarblackdiamond error-barred black diamond
⧯ \errbarblacksquare errbarblacksquare error-barred black square
⧲ \errbarcircle errbarcircle error-barred white circle
⧰ \errbardiamond errbardiamond error-barred white diamond
⧮ \errbarsquare errbarsquare error-barred white square
ℇ \Eulerconst Eulerconst euler constant
€ \euro euro euro sign
‼ \Exclam Exclam double exclamation mark
∃ \exists exists at least one exists
≒ \fallingdotseq fallingdotseq equals, falling dots
⧓ \fbowtie fbowtie black bowtie
⨾ \fcmp fcmp z notation relational composition
⤯ \fdiagovnearrow fdiagovnearrow falling diagonal crossing north east arrow
⤬ \fdiagovrdiag fdiagovrdiag falling diagonal crossing rising diagonal
♀ \female female venus, female
⨏ \fint fint integral average with slash
Ⅎ \Finv Finv turned capital f
◉ \fisheye fisheye fisheye
♭ \flat flat musical flat
⏥ \fltns fltns flatness
∀ \forall forall for all
⫝̸ \forks forks forking
⫝ \forksnot forksnot nonforking
⫙ \forkv forkv element of opening downwards
∜ \fourthroot fourthroot fourth root
⦙ \fourvdots fourvdots dotted fence
⁄ \fracslash fracslash fraction slash
⌢ \frown frown down curve
⟗ \fullouterjoin fullouterjoin full outer join
⅁ \Game Game turned sans-serif capital g
≥ \geq geq /geq /ge r: greater-than-or-equal
≧ \geqq geqq greater, double equals
⫺ \geqqslant geqqslant double-line slanted greater-than or equal to
⩾ \geqslant geqslant greater-than or slanted equal to
⪩ \gescc gescc greater-than closed by curve above slanted equal
⪀ \gesdot gesdot greater-than or slanted equal to with dot inside
⪂ \gesdoto gesdoto greater-than or slanted equal to with dot above
⪄ \gesdotol gesdotol greater-than or slanted equal to with dot above left
⪔ \gesles gesles greater-than above slanted equal above less-than above slanted equal
≫ \gg gg much greater than, type 2
⋙ \ggg ggg /ggg /gg /gggtr r: triple greater-than
⫸ \gggnest gggnest stacked very much greater-than
ℷ \gimel gimel gimel, hebrew
⪥ \gla gla greater-than beside less-than
⪒ \glE glE greater-than above less-than above double-line equal
⧦ \gleichstark gleichstark gleich stark
⪤ \glj glj greater-than overlapping less-than
⪊ \gnapprox gnapprox greater-than and not approximate
⪈ \gneq gneq greater-than and single-line not equal to
≩ \gneqq gneqq greater, not double equals
⋧ \gnsim gnsim greater, not similar
̀ \grave grave grave accent
> \greater greater greater-than sign r:
⪎ \gsime gsime greater-than above similar or equal
⪐ \gsiml gsiml greater-than above similar above less-than
⪢ \Gt Gt double nested greater-than
⪧ \gtcc gtcc greater-than closed by curve
⩺ \gtcir gtcir greater-than with circle inside
⦠ \gtlpar gtlpar spherical angle opening left
⩼ \gtquest gtquest greater-than with question mark above
⪆ \gtrapprox gtrapprox greater-than or approximate
⥸ \gtrarr gtrarr greater-than above rightwards arrow
⋗ \gtrdot gtrdot greater than, with dot
⋛ \gtreqless gtreqless greater, equals, less
⪌ \gtreqqless gtreqqless greater-than above double-line equal above less-than
≷ \gtrless gtrless greater, less
≳ \gtrsim gtrsim greater, similar
⎯ \harrowextender harrowextender horizontal line extension (used to extend arrows)
̂ \hat hat circumflex accent
⩯ \hatapprox hatapprox almost equal to with circumflex accent
♡ \heartsuit heartsuit heart suit symbol
⚥ \Hermaphrodite Hermaphrodite male and female sign
⊹ \hermitmatrix hermitmatrix hermitian conjugate matrix
⎔ \hexagon hexagon horizontal benzene ring [hexagon flat open]
⬣ \hexagonblack hexagonblack horizontal black hexagon
⤤ \hknearrow hknearrow north east arrow with hook
⤣ \hknwarrow hknwarrow north west arrow with hook
⤥ \hksearrow hksearrow south east arrow with hook
⤦ \hkswarrow hkswarrow south west arrow with hook
↩ \hookleftarrow hookleftarrow left arrow-hooked
↪ \hookrightarrow hookrightarrow right arrow-hooked
― \horizbar horizbar horizontal bar
⧖ \hourglass hourglass white hourglass
⌂ \house house house
▭ \hrectangle hrectangle horizontal rectangle, open
▬ \hrectangleblack hrectangleblack black rectangle
ℏ \hslash hslash /hslash - variant planck's over 2pi
⁃ \hyphenbullet hyphenbullet rectangle, filled (hyphen bullet)
〰 \hzigzag hzigzag zigzag
⨌ \iiiint iiiint quadruple integral operator
∭ \iiint iiint triple integral operator
⧜ \iinfin iinfin incomplete infinity
∬ \iint iint double integral operator
ℑ \Im Im imaginary part
⊷ \imageof imageof image of
𝚤 \imath imath mathematical italic small dotless i
∈ \in in set membership, variant
∆ \increment increment laplacian (delta; nabla\string^2)
∞ \infty infty infinity
∫ \int int integral operator
⨍ \intbar intbar finite part integral
⨎ \intBar intBar integral with double stroke
⌡ \intbottom intbottom bottom half integral
⨙ \intcap intcap integral with intersection
∱ \intclockwise intclockwise clockwise integral
⨚ \intcup intcup integral with union
⊺ \intercal intercal intercal
⫴ \interleave interleave triple vertical bar binary relation
⎮ \intextender intextender integral extension
⨗ \intlarhk intlarhk integral with leftwards arrow with hook
⨼ \intprod intprod interior product
⨽ \intprodr intprodr righthand interior product
⌠ \inttop inttop top half integral
⨘ \intx intx integral with times sign
◘ \inversebullet inversebullet inverse bullet
◙ \inversewhitecircle inversewhitecircle inverse white circle
∾ \invlazys invlazys most positive [inverted lazy s]
⌐ \invnot invnot reverse not
◛ \invwhitelowerhalfcircle invwhitelowerhalfcircle lower half inverse white circle
◚ \invwhiteupperhalfcircle invwhiteupperhalfcircle upper half inverse white circle
⋵ \isindot isindot element of with dot above
⋹ \isinE isinE element of with two horizontal strokes
⋷ \isinobar isinobar small element of with overbar
⋴ \isins isins small element of with vertical bar at end of horizontal stroke
⋸ \isinvb isinvb element of with underbar
𝚥 \jmath jmath mathematical italic small dotless j
⨝ \Join Join join
∻ \kernelcontraction kernelcontraction homothetic
⟨ \langle langle mathematical left angle bracket
⟪ \lAngle lAngle mathematical left double angle bracket
⦑ \langledot langledot left angle bracket with dot
⧠ \laplac laplac square with contoured outline
⪫ \lat lat larger than
⪭ \late late larger than or equal to
⟅ \lbag lbag left s-shaped bag delimiter
⦗ \lblkbrbrak lblkbrbrak left black tortoise shell bracket
{ \lbrace lbrace left curly bracket
⦃ \lBrace lBrace left white curly bracket
⎩ \lbracelend lbracelend left curly bracket lower hook
⎨ \lbracemid lbracemid left curly bracket middle piece
⎧ \lbraceuend lbraceuend left curly bracket upper hook
[ \lbrack lbrack left square bracket
⟦ \lBrack lBrack mathematical left white square bracket
⎢ \lbrackextender lbrackextender left square bracket extension
⎣ \lbracklend lbracklend left square bracket lower corner
⦏ \lbracklltick lbracklltick left square bracket with tick in bottom corner
⦋ \lbrackubar lbrackubar left square bracket with underbar
⎡ \lbrackuend lbrackuend left square bracket upper corner
⦍ \lbrackultick lbrackultick left square bracket with tick in top corner
❲ \lbrbrak lbrbrak light left tortoise shell bracket ornament
⟬ \Lbrbrak Lbrbrak mathematical left white tortoise shell bracket
⌈ \lceil lceil left ceiling
⧼ \lcurvyangle lcurvyangle left pointing curved angle bracket
↲ \Ldsh Ldsh left down angled arrow
← \leftarrow leftarrow /leftarrow /gets a: leftward arrow
⇐ \Leftarrow Leftarrow is implied by
⭊ \leftarrowapprox leftarrowapprox leftwards arrow above almost equal to
⭂ \leftarrowbackapprox leftarrowbackapprox leftwards arrow above reverse almost equal to
⭋ \leftarrowbsimilar leftarrowbsimilar leftwards arrow above reverse tilde operator
⥷ \leftarrowless leftarrowless leftwards arrow through less-than
⬲ \leftarrowonoplus leftarrowonoplus left arrow with circled plus
⥆ \leftarrowplus leftarrowplus leftwards arrow with plus below
⥃ \leftarrowshortrightarrow leftarrowshortrightarrow leftwards arrow above short rightwards arrow
⥳ \leftarrowsimilar leftarrowsimilar leftwards arrow above tilde operator
⥺ \leftarrowsubset leftarrowsubset leftwards arrow through subset
↢ \leftarrowtail leftarrowtail left arrow-tailed
⇽ \leftarrowtriangle leftarrowtriangle leftwards open-headed arrow
⬾ \leftarrowx leftarrowx leftwards arrow through x
⤌ \leftbkarrow leftbkarrow leftwards double dash arrow
⬿ \leftcurvedarrow leftcurvedarrow wave arrow pointing directly left
⇠ \leftdasharrow leftdasharrow leftwards dashed arrow
⤎ \leftdbkarrow leftdbkarrow leftwards triple dash arrow
⤛ \leftdbltail leftdbltail leftwards double arrow-tail
⬸ \leftdotarrow leftdotarrow leftwards arrow with dotted stem
⤶ \leftdowncurvedarrow leftdowncurvedarrow arrow pointing downwards then curving leftwards
⥼ \leftfishtail leftfishtail left fish tail
⃐ \leftharpoonaccent leftharpoonaccent combining left harpoon above
↽ \leftharpoondown leftharpoondown left harpoon-down
⥞ \leftharpoondownbar leftharpoondownbar leftwards harpoon with barb down from bar
⥢ \leftharpoonsupdown leftharpoonsupdown leftwards harpoon with barb up above leftwards harpoon with barb down
↼ \leftharpoonup leftharpoonup left harpoon-up
⥚ \leftharpoonupbar leftharpoonupbar leftwards harpoon with barb up from bar
⥪ \leftharpoonupdash leftharpoonupdash leftwards harpoon with barb up above long dash
⇇ \leftleftarrows leftleftarrows two left arrows
☾ \leftmoon leftmoon last quarter moon
⟕ \leftouterjoin leftouterjoin left outer join
↔ \leftrightarrow leftrightarrow left and right arrow
⇔ \Leftrightarrow Leftrightarrow left and right double arrow
⥈ \leftrightarrowcircle leftrightarrowcircle left right arrow through small circle
⇆ \leftrightarrows leftrightarrows left arrow over right arrow
⇿ \leftrightarrowtriangle leftrightarrowtriangle left right open-headed arrow
⥐ \leftrightharpoondowndown leftrightharpoondowndown left barb down right barb down harpoon
⥋ \leftrightharpoondownup leftrightharpoondownup left barb down right barb up harpoon
⇋ \leftrightharpoons leftrightharpoons left harpoon over right
⥧ \leftrightharpoonsdown leftrightharpoonsdown leftwards harpoon with barb down above rightwards harpoon with barb down
⥦ \leftrightharpoonsup leftrightharpoonsup leftwards harpoon with barb up above rightwards harpoon with barb up
⥊ \leftrightharpoonupdown leftrightharpoonupdown left barb up right barb down harpoon
⥎ \leftrightharpoonupup leftrightharpoonupup left barb up right barb up harpoon
↭ \leftrightsquigarrow leftrightsquigarrow left and right arr-wavy
⇜ \leftsquigarrow leftsquigarrow leftwards squiggle arrow
⤙ \lefttail lefttail leftwards arrow-tail
⬱ \leftthreearrows leftthreearrows three leftwards arrows
⋋ \leftthreetimes leftthreetimes left semidirect product
↜ \leftwavearrow leftwavearrow left arrow-wavy
⇦ \leftwhitearrow leftwhitearrow leftwards white arrow
≤ \leq leq /leq /le r: less-than-or-equal
≦ \leqq leqq less, double equals
⫹ \leqqslant leqqslant double-line slanted less-than or equal to
⩽ \leqslant leqslant less-than or slanted equal to
⪨ \lescc lescc less-than closed by curve above slanted equal
⩿ \lesdot lesdot less-than or slanted equal to with dot inside
⪁ \lesdoto lesdoto less-than or slanted equal to with dot above
⪃ \lesdotor lesdotor less-than or slanted equal to with dot above right
⪓ \lesges lesges less-than above slanted equal above greater-than above slanted equal
< \less less less-than sign r:
⪅ \lessapprox lessapprox less-than or approximate
⋖ \lessdot lessdot less than, with dot
⋚ \lesseqgtr lesseqgtr less, equals, greater
⪋ \lesseqqgtr lesseqqgtr less-than above double-line equal above greater-than
≶ \lessgtr lessgtr less, greater
≲ \lesssim lesssim less, similar
⧑ \lfbowtie lfbowtie left black bowtie
⌊ \lfloor lfloor left floor
⧔ \lftimes lftimes left black times
⬤ \lgblkcircle lgblkcircle black large circle
⬛ \lgblksquare lgblksquare black large square
⪑ \lgE lgE less-than above greater-than above double-line equal
⟮ \lgroup lgroup mathematical left flattened parenthesis
◯ \lgwhtcircle lgwhtcircle large circle
⬜ \lgwhtsquare lgwhtsquare white large square
↴ \linefeed linefeed rightwards arrow with corner downwards
≪ \ll ll much less than, type 2
⦉ \llangle llangle z notation left binding bracket
◟ \llarc llarc lower left quadrant circular arc
◣ \llblacktriangle llblacktriangle lower left triangle, filled
⌞ \llcorner llcorner lower left corner
⇚ \Lleftarrow Lleftarrow left triple arrow
⭅ \LLeftarrow LLeftarrow leftwards quadruple arrow
⋘ \lll lll /ll /lll /llless r: triple less-than
⫷ \lllnest lllnest stacked very much less-than
⦇ \llparenthesis llparenthesis z notation left image bracket
◺ \lltriangle lltriangle lower left triangle
⎰ \lmoustache lmoustache upper left or lower right curly bracket section
⪉ \lnapprox lnapprox less-than and not approximate
⪇ \lneq lneq less-than and single-line not equal to
≨ \lneqq lneqq less, not double equals
⋦ \lnsim lnsim less, not similar
⟞ \longdashv longdashv long right tack
⟌ \longdivision longdivision long division
⟵ \longleftarrow longleftarrow long leftwards arrow
⟸ \Longleftarrow Longleftarrow long leftwards double arrow
⟷ \longleftrightarrow longleftrightarrow long left right arrow
⟺ \Longleftrightarrow Longleftrightarrow long left right double arrow
⬳ \longleftsquigarrow longleftsquigarrow long leftwards squiggle arrow
⟻ \longmapsfrom longmapsfrom long leftwards arrow from bar
⟽ \Longmapsfrom Longmapsfrom long leftwards double arrow from bar
⟼ \longmapsto longmapsto long rightwards arrow from bar
⟾ \Longmapsto Longmapsto long rightwards double arrow from bar
⟶ \longrightarrow longrightarrow long rightwards arrow
⟹ \Longrightarrow Longrightarrow long rightwards double arrow
⟿ \longrightsquigarrow longrightsquigarrow long rightwards squiggle arrow
↫ \looparrowleft looparrowleft left arrow-looped
↬ \looparrowright looparrowright right arrow-looped
⨜ \lowint lowint integral with underbar
⟠ \lozengeminus lozengeminus lozenge divided by horizontal rule
( \lparen lparen left parenthesis
⦅ \lParen lParen left white parenthesis
⎜ \lparenextender lparenextender left parenthesis extension
⦕ \Lparengtr Lparengtr double left arc greater-than bracket
⎝ \lparenlend lparenlend left parenthesis lower hook
⦓ \lparenless lparenless left arc less-than bracket
⎛ \lparenuend lparenuend left parenthesis upper hook
◞ \lrarc lrarc lower right quadrant circular arc
◢ \lrblacktriangle lrblacktriangle lower right triangle, filled
⌟ \lrcorner lrcorner lower right corner
◿ \lrtriangle lrtriangle lower right triangle
⧡ \lrtriangleeq lrtriangleeq increases as
↰ \Lsh Lsh /lsh a:
⪍ \lsime lsime less-than above similar or equal
⪏ \lsimg lsimg less-than above similar above greater-than
⫍ \lsqhook lsqhook square left open box operator
⪡ \Lt Lt double nested less-than
⪦ \ltcc ltcc less-than closed by curve
⩹ \ltcir ltcir less-than with circle inside
⋉ \ltimes ltimes times sign, left closed
⥶ \ltlarr ltlarr less-than above leftwards arrow
⩻ \ltquest ltquest less-than with question mark above
⧏ \ltrivb ltrivb left triangle beside vertical bar
⎸ \lvboxline lvboxline left vertical box line
⧘ \lvzigzag lvzigzag left wiggly fence
⧚ \Lvzigzag Lvzigzag left double wiggly fence
♂ \male male mars, male
✠ \maltese maltese maltese cross
↧ \mapsdown mapsdown maps to, downward
↤ \mapsfrom mapsfrom maps to, leftward
⤆ \Mapsfrom Mapsfrom leftwards double arrow from bar
↦ \mapsto mapsto maps to, rightward
⤇ \Mapsto Mapsto rightwards double arrow from bar
↥ \mapsup mapsup maps to, upward
& \mathampersand mathampersand ampersand
@ \mathatsign mathatsign commercial at
: \mathcolon mathcolon colon
, \mathcomma mathcomma comma
$ \mathdollar mathdollar dollar sign
ð \matheth matheth eth
! \mathexclam mathexclam exclamation mark
‐ \mathhyphen mathhyphen hyphen
# \mathoctothorpe mathoctothorpe number sign
¶ \mathparagraph mathparagraph paragraph symbol
% \mathpercent mathpercent percent sign
. \mathperiod mathperiod full stop, period
+ \mathplus mathplus plus sign b:
? \mathquestion mathquestion question mark
∶ \mathratio mathratio ratio
§ \mathsection mathsection section symbol
; \mathsemicolon mathsemicolon semicolon p:
/ \mathslash mathslash solidus
£ \mathsterling mathsterling pound sign
̲ \mathunderbar mathunderbar combining low line
␣ \mathvisiblespace mathvisiblespace open box
¥ \mathyen mathyen yen sign
𝐚 \mbfa mbfa mathematical bold small a
𝐀 \mbfA mbfA mathematical bold capital a
𝛂 \mbfalpha mbfalpha mathematical bold small alpha
𝚨 \mbfAlpha mbfAlpha mathematical bold capital alpha
𝐛 \mbfb mbfb mathematical bold small b
𝐁 \mbfB mbfB mathematical bold capital b
𝛃 \mbfbeta mbfbeta mathematical bold small beta
𝚩 \mbfBeta mbfBeta mathematical bold capital beta
𝐜 \mbfc mbfc mathematical bold small c
𝐂 \mbfC mbfC mathematical bold capital c
𝛘 \mbfchi mbfchi mathematical bold small chi
𝚾 \mbfChi mbfChi mathematical bold capital chi
𝐝 \mbfd mbfd mathematical bold small d
𝐃 \mbfD mbfD mathematical bold capital d
𝛅 \mbfdelta mbfdelta mathematical bold small delta
𝚫 \mbfDelta mbfDelta mathematical bold capital delta
𝟋 \mbfdigamma mbfdigamma mathematical bold small digamma
𝟊 \mbfDigamma mbfDigamma mathematical bold capital digamma
𝐞 \mbfe mbfe mathematical bold small e
𝐄 \mbfE mbfE mathematical bold capital e
𝟖 \mbfeight mbfeight mathematical bold digit 8
𝛜 \mbfepsilon mbfepsilon mathematical bold varepsilon symbol
𝚬 \mbfEpsilon mbfEpsilon mathematical bold capital epsilon
𝛈 \mbfeta mbfeta mathematical bold small eta
𝚮 \mbfEta mbfEta mathematical bold capital eta
𝐟 \mbff mbff mathematical bold small f
𝐅 \mbfF mbfF mathematical bold capital f
𝟓 \mbffive mbffive mathematical bold digit 5
𝟒 \mbffour mbffour mathematical bold digit 4
𝖆 \mbffraka mbffraka mathematical bold fraktur small a
𝕬 \mbffrakA mbffrakA mathematical bold fraktur capital a
𝖇 \mbffrakb mbffrakb mathematical bold fraktur small b
𝕭 \mbffrakB mbffrakB mathematical bold fraktur capital b
𝖈 \mbffrakc mbffrakc mathematical bold fraktur small c
𝕮 \mbffrakC mbffrakC mathematical bold fraktur capital c
𝖉 \mbffrakd mbffrakd mathematical bold fraktur small d
𝕯 \mbffrakD mbffrakD mathematical bold fraktur capital d
𝖊 \mbffrake mbffrake mathematical bold fraktur small e
𝕰 \mbffrakE mbffrakE mathematical bold fraktur capital e
𝖋 \mbffrakf mbffrakf mathematical bold fraktur small f
𝕱 \mbffrakF mbffrakF mathematical bold fraktur capital f
𝖌 \mbffrakg mbffrakg mathematical bold fraktur small g
𝕲 \mbffrakG mbffrakG mathematical bold fraktur capital g
𝖍 \mbffrakh mbffrakh mathematical bold fraktur small h
𝕳 \mbffrakH mbffrakH mathematical bold fraktur capital h
𝖎 \mbffraki mbffraki mathematical bold fraktur small i
𝕴 \mbffrakI mbffrakI mathematical bold fraktur capital i
𝖏 \mbffrakj mbffrakj mathematical bold fraktur small j
𝕵 \mbffrakJ mbffrakJ mathematical bold fraktur capital j
𝖐 \mbffrakk mbffrakk mathematical bold fraktur small k
𝕶 \mbffrakK mbffrakK mathematical bold fraktur capital k
𝖑 \mbffrakl mbffrakl mathematical bold fraktur small l
𝕷 \mbffrakL mbffrakL mathematical bold fraktur capital l
𝖒 \mbffrakm mbffrakm mathematical bold fraktur small m
𝕸 \mbffrakM mbffrakM mathematical bold fraktur capital m
𝖓 \mbffrakn mbffrakn mathematical bold fraktur small n
𝕹 \mbffrakN mbffrakN mathematical bold fraktur capital n
𝖔 \mbffrako mbffrako mathematical bold fraktur small o
𝕺 \mbffrakO mbffrakO mathematical bold fraktur capital o
𝖕 \mbffrakp mbffrakp mathematical bold fraktur small p
𝕻 \mbffrakP mbffrakP mathematical bold fraktur capital p
𝖖 \mbffrakq mbffrakq mathematical bold fraktur small q
𝕼 \mbffrakQ mbffrakQ mathematical bold fraktur capital q
𝖗 \mbffrakr mbffrakr mathematical bold fraktur small r
𝕽 \mbffrakR mbffrakR mathematical bold fraktur capital r
𝖘 \mbffraks mbffraks mathematical bold fraktur small s
𝕾 \mbffrakS mbffrakS mathematical bold fraktur capital s
𝖙 \mbffrakt mbffrakt mathematical bold fraktur small t
𝕿 \mbffrakT mbffrakT mathematical bold fraktur capital t
𝖚 \mbffraku mbffraku mathematical bold fraktur small u
𝖀 \mbffrakU mbffrakU mathematical bold fraktur capital u
𝖛 \mbffrakv mbffrakv mathematical bold fraktur small v
𝖁 \mbffrakV mbffrakV mathematical bold fraktur capital v
𝖜 \mbffrakw mbffrakw mathematical bold fraktur small w
𝖂 \mbffrakW mbffrakW mathematical bold fraktur capital w
𝖝 \mbffrakx mbffrakx mathematical bold fraktur small x
𝖃 \mbffrakX mbffrakX mathematical bold fraktur capital x
𝖞 \mbffraky mbffraky mathematical bold fraktur small y
𝖄 \mbffrakY mbffrakY mathematical bold fraktur capital y
𝖟 \mbffrakz mbffrakz mathematical bold fraktur small z
𝖅 \mbffrakZ mbffrakZ mathematical bold fraktur capital z
𝐠 \mbfg mbfg mathematical bold small g
𝐆 \mbfG mbfG mathematical bold capital g
𝛄 \mbfgamma mbfgamma mathematical bold small gamma
𝚪 \mbfGamma mbfGamma mathematical bold capital gamma
𝐡 \mbfh mbfh mathematical bold small h
𝐇 \mbfH mbfH mathematical bold capital h
𝐢 \mbfi mbfi mathematical bold small i
𝐈 \mbfI mbfI mathematical bold capital i
𝛊 \mbfiota mbfiota mathematical bold small iota
𝚰 \mbfIota mbfIota mathematical bold capital iota
𝒂 \mbfita mbfita mathematical bold italic small a
𝑨 \mbfitA mbfitA mathematical bold italic capital a
𝜶 \mbfitalpha mbfitalpha mathematical bold italic small alpha
𝜜 \mbfitAlpha mbfitAlpha mathematical bold italic capital alpha
𝒃 \mbfitb mbfitb mathematical bold italic small b
𝑩 \mbfitB mbfitB mathematical bold italic capital b
𝜷 \mbfitbeta mbfitbeta mathematical bold italic small beta
𝜝 \mbfitBeta mbfitBeta mathematical bold italic capital beta
𝒄 \mbfitc mbfitc mathematical bold italic small c
𝑪 \mbfitC mbfitC mathematical bold italic capital c
𝝌 \mbfitchi mbfitchi mathematical bold italic small chi
𝜲 \mbfitChi mbfitChi mathematical bold italic capital chi
𝒅 \mbfitd mbfitd mathematical bold italic small d
𝑫 \mbfitD mbfitD mathematical bold italic capital d
𝜹 \mbfitdelta mbfitdelta mathematical bold italic small delta
𝜟 \mbfitDelta mbfitDelta mathematical bold italic capital delta
𝒆 \mbfite mbfite mathematical bold italic small e
𝑬 \mbfitE mbfitE mathematical bold italic capital e
𝝐 \mbfitepsilon mbfitepsilon mathematical bold italic varepsilon symbol
𝜠 \mbfitEpsilon mbfitEpsilon mathematical bold italic capital epsilon
𝜼 \mbfiteta mbfiteta mathematical bold italic small eta
𝜢 \mbfitEta mbfitEta mathematical bold italic capital eta
𝒇 \mbfitf mbfitf mathematical bold italic small f
𝑭 \mbfitF mbfitF mathematical bold italic capital f
𝒈 \mbfitg mbfitg mathematical bold italic small g
𝑮 \mbfitG mbfitG mathematical bold italic capital g
𝜸 \mbfitgamma mbfitgamma mathematical bold italic small gamma
𝜞 \mbfitGamma mbfitGamma mathematical bold italic capital gamma
𝒉 \mbfith mbfith mathematical bold italic small h
𝑯 \mbfitH mbfitH mathematical bold italic capital h
𝒊 \mbfiti mbfiti mathematical bold italic small i
𝑰 \mbfitI mbfitI mathematical bold italic capital i
𝜾 \mbfitiota mbfitiota mathematical bold italic small iota
𝜤 \mbfitIota mbfitIota mathematical bold italic capital iota
𝒋 \mbfitj mbfitj mathematical bold italic small j
𝑱 \mbfitJ mbfitJ mathematical bold italic capital j
𝒌 \mbfitk mbfitk mathematical bold italic small k
𝑲 \mbfitK mbfitK mathematical bold italic capital k
𝜿 \mbfitkappa mbfitkappa mathematical bold italic small kappa
𝜥 \mbfitKappa mbfitKappa mathematical bold italic capital kappa
𝒍 \mbfitl mbfitl mathematical bold italic small l
𝑳 \mbfitL mbfitL mathematical bold italic capital l
𝝀 \mbfitlambda mbfitlambda mathematical bold italic small lambda
𝜦 \mbfitLambda mbfitLambda mathematical bold italic capital lambda
𝒎 \mbfitm mbfitm mathematical bold italic small m
𝑴 \mbfitM mbfitM mathematical bold italic capital m
𝝁 \mbfitmu mbfitmu mathematical bold italic small mu
𝜧 \mbfitMu mbfitMu mathematical bold italic capital mu
𝒏 \mbfitn mbfitn mathematical bold italic small n
𝑵 \mbfitN mbfitN mathematical bold italic capital n
𝜵 \mbfitnabla mbfitnabla mathematical bold italic nabla
𝝂 \mbfitnu mbfitnu mathematical bold italic small nu
𝜨 \mbfitNu mbfitNu mathematical bold italic capital nu
𝒐 \mbfito mbfito mathematical bold italic small o
𝑶 \mbfitO mbfitO mathematical bold italic capital o
𝝎 \mbfitomega mbfitomega mathematical bold italic small omega
𝜴 \mbfitOmega mbfitOmega mathematical bold italic capital omega
𝝄 \mbfitomicron mbfitomicron mathematical bold italic small omicron
𝜪 \mbfitOmicron mbfitOmicron mathematical bold italic capital omicron
𝒑 \mbfitp mbfitp mathematical bold italic small p
𝑷 \mbfitP mbfitP mathematical bold italic capital p
𝝏 \mbfitpartial mbfitpartial mathematical bold italic partial differential
𝝓 \mbfitphi mbfitphi mathematical bold italic phi symbol
𝜱 \mbfitPhi mbfitPhi mathematical bold italic capital phi
𝝅 \mbfitpi mbfitpi mathematical bold italic small pi
𝜫 \mbfitPi mbfitPi mathematical bold italic capital pi
𝝍 \mbfitpsi mbfitpsi mathematical bold italic small psi
𝜳 \mbfitPsi mbfitPsi mathematical bold italic capital psi
𝒒 \mbfitq mbfitq mathematical bold italic small q
𝑸 \mbfitQ mbfitQ mathematical bold italic capital q
𝒓 \mbfitr mbfitr mathematical bold italic small r
𝑹 \mbfitR mbfitR mathematical bold italic capital r
𝝆 \mbfitrho mbfitrho mathematical bold italic small rho
𝜬 \mbfitRho mbfitRho mathematical bold italic capital rho
𝒔 \mbfits mbfits mathematical bold italic small s
𝑺 \mbfitS mbfitS mathematical bold italic capital s
𝙖 \mbfitsansa mbfitsansa mathematical sans-serif bold italic small a
𝘼 \mbfitsansA mbfitsansA mathematical sans-serif bold italic capital a
𝞪 \mbfitsansalpha mbfitsansalpha mathematical sans-serif bold italic small alpha
𝞐 \mbfitsansAlpha mbfitsansAlpha mathematical sans-serif bold italic capital alpha
𝙗 \mbfitsansb mbfitsansb mathematical sans-serif bold italic small b
𝘽 \mbfitsansB mbfitsansB mathematical sans-serif bold italic capital b
𝞫 \mbfitsansbeta mbfitsansbeta mathematical sans-serif bold italic small beta
𝞑 \mbfitsansBeta mbfitsansBeta mathematical sans-serif bold italic capital beta
𝙘 \mbfitsansc mbfitsansc mathematical sans-serif bold italic small c
𝘾 \mbfitsansC mbfitsansC mathematical sans-serif bold italic capital c
𝟀 \mbfitsanschi mbfitsanschi mathematical sans-serif bold italic small chi
𝞦 \mbfitsansChi mbfitsansChi mathematical sans-serif bold italic capital chi
𝙙 \mbfitsansd mbfitsansd mathematical sans-serif bold italic small d
𝘿 \mbfitsansD mbfitsansD mathematical sans-serif bold italic capital d
𝞭 \mbfitsansdelta mbfitsansdelta mathematical sans-serif bold italic small delta
𝞓 \mbfitsansDelta mbfitsansDelta mathematical sans-serif bold italic capital delta
𝙚 \mbfitsanse mbfitsanse mathematical sans-serif bold italic small e
𝙀 \mbfitsansE mbfitsansE mathematical sans-serif bold italic capital e
𝟄 \mbfitsansepsilon mbfitsansepsilon mathematical sans-serif bold italic varepsilon symbol
𝞔 \mbfitsansEpsilon mbfitsansEpsilon mathematical sans-serif bold italic capital epsilon
𝞰 \mbfitsanseta mbfitsanseta mathematical sans-serif bold italic small eta
𝞖 \mbfitsansEta mbfitsansEta mathematical sans-serif bold italic capital eta
𝙛 \mbfitsansf mbfitsansf mathematical sans-serif bold italic small f
𝙁 \mbfitsansF mbfitsansF mathematical sans-serif bold italic capital f
𝙜 \mbfitsansg mbfitsansg mathematical sans-serif bold italic small g
𝙂 \mbfitsansG mbfitsansG mathematical sans-serif bold italic capital g
𝞬 \mbfitsansgamma mbfitsansgamma mathematical sans-serif bold italic small gamma
𝞒 \mbfitsansGamma mbfitsansGamma mathematical sans-serif bold italic capital gamma
𝙝 \mbfitsansh mbfitsansh mathematical sans-serif bold italic small h
𝙃 \mbfitsansH mbfitsansH mathematical sans-serif bold italic capital h
𝙞 \mbfitsansi mbfitsansi mathematical sans-serif bold italic small i
𝙄 \mbfitsansI mbfitsansI mathematical sans-serif bold italic capital i
𝞲 \mbfitsansiota mbfitsansiota mathematical sans-serif bold italic small iota
𝞘 \mbfitsansIota mbfitsansIota mathematical sans-serif bold italic capital iota
𝙟 \mbfitsansj mbfitsansj mathematical sans-serif bold italic small j
𝙅 \mbfitsansJ mbfitsansJ mathematical sans-serif bold italic capital j
𝙠 \mbfitsansk mbfitsansk mathematical sans-serif bold italic small k
𝙆 \mbfitsansK mbfitsansK mathematical sans-serif bold italic capital k
𝞳 \mbfitsanskappa mbfitsanskappa mathematical sans-serif bold italic small kappa
𝞙 \mbfitsansKappa mbfitsansKappa mathematical sans-serif bold italic capital kappa
𝙡 \mbfitsansl mbfitsansl mathematical sans-serif bold italic small l
𝙇 \mbfitsansL mbfitsansL mathematical sans-serif bold italic capital l
𝞴 \mbfitsanslambda mbfitsanslambda mathematical sans-serif bold italic small lambda
𝞚 \mbfitsansLambda mbfitsansLambda mathematical sans-serif bold italic capital lambda
𝙢 \mbfitsansm mbfitsansm mathematical sans-serif bold italic small m
𝙈 \mbfitsansM mbfitsansM mathematical sans-serif bold italic capital m
𝞵 \mbfitsansmu mbfitsansmu mathematical sans-serif bold italic small mu
𝞛 \mbfitsansMu mbfitsansMu mathematical sans-serif bold italic capital mu
𝙣 \mbfitsansn mbfitsansn mathematical sans-serif bold italic small n
𝙉 \mbfitsansN mbfitsansN mathematical sans-serif bold italic capital n
𝞩 \mbfitsansnabla mbfitsansnabla mathematical sans-serif bold italic nabla
𝞶 \mbfitsansnu mbfitsansnu mathematical sans-serif bold italic small nu
𝞜 \mbfitsansNu mbfitsansNu mathematical sans-serif bold italic capital nu
𝙤 \mbfitsanso mbfitsanso mathematical sans-serif bold italic small o
𝙊 \mbfitsansO mbfitsansO mathematical sans-serif bold italic capital o
𝟂 \mbfitsansomega mbfitsansomega mathematical sans-serif bold italic small omega
𝞨 \mbfitsansOmega mbfitsansOmega mathematical sans-serif bold italic capital omega
𝞸 \mbfitsansomicron mbfitsansomicron mathematical sans-serif bold italic small omicron
𝞞 \mbfitsansOmicron mbfitsansOmicron mathematical sans-serif bold italic capital omicron
𝙥 \mbfitsansp mbfitsansp mathematical sans-serif bold italic small p
𝙋 \mbfitsansP mbfitsansP mathematical sans-serif bold italic capital p
𝟃 \mbfitsanspartial mbfitsanspartial mathematical sans-serif bold italic partial differential
𝟇 \mbfitsansphi mbfitsansphi mathematical sans-serif bold italic phi symbol
𝞥 \mbfitsansPhi mbfitsansPhi mathematical sans-serif bold italic capital phi
𝞹 \mbfitsanspi mbfitsanspi mathematical sans-serif bold italic small pi
𝞟 \mbfitsansPi mbfitsansPi mathematical sans-serif bold italic capital pi
𝟁 \mbfitsanspsi mbfitsanspsi mathematical sans-serif bold italic small psi
𝞧 \mbfitsansPsi mbfitsansPsi mathematical sans-serif bold italic capital psi
𝙦 \mbfitsansq mbfitsansq mathematical sans-serif bold italic small q
𝙌 \mbfitsansQ mbfitsansQ mathematical sans-serif bold italic capital q
𝙧 \mbfitsansr mbfitsansr mathematical sans-serif bold italic small r
𝙍 \mbfitsansR mbfitsansR mathematical sans-serif bold italic capital r
𝞺 \mbfitsansrho mbfitsansrho mathematical sans-serif bold italic small rho
𝞠 \mbfitsansRho mbfitsansRho mathematical sans-serif bold italic capital rho
𝙨 \mbfitsanss mbfitsanss mathematical sans-serif bold italic small s
𝙎 \mbfitsansS mbfitsansS mathematical sans-serif bold italic capital s
𝞼 \mbfitsanssigma mbfitsanssigma mathematical sans-serif bold italic small sigma
𝞢 \mbfitsansSigma mbfitsansSigma mathematical sans-serif bold italic capital sigma
𝙩 \mbfitsanst mbfitsanst mathematical sans-serif bold italic small t
𝙏 \mbfitsansT mbfitsansT mathematical sans-serif bold italic capital t
𝞽 \mbfitsanstau mbfitsanstau mathematical sans-serif bold italic small tau
𝞣 \mbfitsansTau mbfitsansTau mathematical sans-serif bold italic capital tau
𝞱 \mbfitsanstheta mbfitsanstheta mathematical sans-serif bold italic small theta
𝞗 \mbfitsansTheta mbfitsansTheta mathematical sans-serif bold italic capital theta
𝙪 \mbfitsansu mbfitsansu mathematical sans-serif bold italic small u
𝙐 \mbfitsansU mbfitsansU mathematical sans-serif bold italic capital u
𝞾 \mbfitsansupsilon mbfitsansupsilon mathematical sans-serif bold italic small upsilon
𝞤 \mbfitsansUpsilon mbfitsansUpsilon mathematical sans-serif bold italic capital upsilon
𝙫 \mbfitsansv mbfitsansv mathematical sans-serif bold italic small v
𝙑 \mbfitsansV mbfitsansV mathematical sans-serif bold italic capital v
𝞮 \mbfitsansvarepsilon mbfitsansvarepsilon mathematical sans-serif bold italic small varepsilon
𝟆 \mbfitsansvarkappa mbfitsansvarkappa mathematical sans-serif bold italic kappa symbol
𝞿 \mbfitsansvarphi mbfitsansvarphi mathematical sans-serif bold italic small phi
𝟉 \mbfitsansvarpi mbfitsansvarpi mathematical sans-serif bold italic pi symbol
𝟈 \mbfitsansvarrho mbfitsansvarrho mathematical sans-serif bold italic rho symbol
𝞻 \mbfitsansvarsigma mbfitsansvarsigma mathematical sans-serif bold italic small final sigma
𝟅 \mbfitsansvartheta mbfitsansvartheta mathematical sans-serif bold italic theta symbol
𝞡 \mbfitsansvarTheta mbfitsansvarTheta mathematical sans-serif bold italic capital theta symbol
𝙬 \mbfitsansw mbfitsansw mathematical sans-serif bold italic small w
𝙒 \mbfitsansW mbfitsansW mathematical sans-serif bold italic capital w
𝙭 \mbfitsansx mbfitsansx mathematical sans-serif bold italic small x
𝙓 \mbfitsansX mbfitsansX mathematical sans-serif bold italic capital x
𝞷 \mbfitsansxi mbfitsansxi mathematical sans-serif bold italic small xi
𝞝 \mbfitsansXi mbfitsansXi mathematical sans-serif bold italic capital xi
𝙮 \mbfitsansy mbfitsansy mathematical sans-serif bold italic small y
𝙔 \mbfitsansY mbfitsansY mathematical sans-serif bold italic capital y
𝙯 \mbfitsansz mbfitsansz mathematical sans-serif bold italic small z
𝙕 \mbfitsansZ mbfitsansZ mathematical sans-serif bold italic capital z
𝞯 \mbfitsanszeta mbfitsanszeta mathematical sans-serif bold italic small zeta
𝞕 \mbfitsansZeta mbfitsansZeta mathematical sans-serif bold italic capital zeta
𝝈 \mbfitsigma mbfitsigma mathematical bold italic small sigma
𝜮 \mbfitSigma mbfitSigma mathematical bold italic capital sigma
𝒕 \mbfitt mbfitt mathematical bold italic small t
𝑻 \mbfitT mbfitT mathematical bold italic capital t
𝝉 \mbfittau mbfittau mathematical bold italic small tau
𝜯 \mbfitTau mbfitTau mathematical bold italic capital tau
𝜽 \mbfittheta mbfittheta mathematical bold italic small theta
𝜣 \mbfitTheta mbfitTheta mathematical bold italic capital theta
𝒖 \mbfitu mbfitu mathematical bold italic small u
𝑼 \mbfitU mbfitU mathematical bold italic capital u
𝝊 \mbfitupsilon mbfitupsilon mathematical bold italic small upsilon
𝜰 \mbfitUpsilon mbfitUpsilon mathematical bold italic capital upsilon
𝒗 \mbfitv mbfitv mathematical bold italic small v
𝑽 \mbfitV mbfitV mathematical bold italic capital v
𝜺 \mbfitvarepsilon mbfitvarepsilon mathematical bold italic small varepsilon
𝝒 \mbfitvarkappa mbfitvarkappa mathematical bold italic kappa symbol
𝝋 \mbfitvarphi mbfitvarphi mathematical bold italic small phi
𝝕 \mbfitvarpi mbfitvarpi mathematical bold italic pi symbol
𝝔 \mbfitvarrho mbfitvarrho mathematical bold italic rho symbol
𝝇 \mbfitvarsigma mbfitvarsigma mathematical bold italic small final sigma
𝝑 \mbfitvartheta mbfitvartheta mathematical bold italic theta symbol
𝜭 \mbfitvarTheta mbfitvarTheta mathematical bold italic capital theta symbol
𝒘 \mbfitw mbfitw mathematical bold italic small w
𝑾 \mbfitW mbfitW mathematical bold italic capital w
𝒙 \mbfitx mbfitx mathematical bold italic small x
𝑿 \mbfitX mbfitX mathematical bold italic capital x
𝝃 \mbfitxi mbfitxi mathematical bold italic small xi
𝜩 \mbfitXi mbfitXi mathematical bold italic capital xi
𝒚 \mbfity mbfity mathematical bold italic small y
𝒀 \mbfitY mbfitY mathematical bold italic capital y
𝒛 \mbfitz mbfitz mathematical bold italic small z
𝒁 \mbfitZ mbfitZ mathematical bold italic capital z
𝜻 \mbfitzeta mbfitzeta mathematical bold italic small zeta
𝜡 \mbfitZeta mbfitZeta mathematical bold italic capital zeta
𝐣 \mbfj mbfj mathematical bold small j
𝐉 \mbfJ mbfJ mathematical bold capital j
𝐤 \mbfk mbfk mathematical bold small k
𝐊 \mbfK mbfK mathematical bold capital k
𝛋 \mbfkappa mbfkappa mathematical bold small kappa
𝚱 \mbfKappa mbfKappa mathematical bold capital kappa
𝐥 \mbfl mbfl mathematical bold small l
𝐋 \mbfL mbfL mathematical bold capital l
𝛌 \mbflambda mbflambda mathematical bold small lambda
𝚲 \mbfLambda mbfLambda mathematical bold capital lambda
𝐦 \mbfm mbfm mathematical bold small m
𝐌 \mbfM mbfM mathematical bold capital m
𝛍 \mbfmu mbfmu mathematical bold small mu
𝚳 \mbfMu mbfMu mathematical bold capital mu
𝐧 \mbfn mbfn mathematical bold small n
𝐍 \mbfN mbfN mathematical bold capital n
𝛁 \mbfnabla mbfnabla mathematical bold nabla
𝟗 \mbfnine mbfnine mathematical bold digit 9
𝛎 \mbfnu mbfnu mathematical bold small nu
𝚴 \mbfNu mbfNu mathematical bold capital nu
𝐨 \mbfo mbfo mathematical bold small o
𝐎 \mbfO mbfO mathematical bold capital o
𝛚 \mbfomega mbfomega mathematical bold small omega
𝛀 \mbfOmega mbfOmega mathematical bold capital omega
𝛐 \mbfomicron mbfomicron mathematical bold small omicron
𝚶 \mbfOmicron mbfOmicron mathematical bold capital omicron
𝟏 \mbfone mbfone mathematical bold digit 1
𝐩 \mbfp mbfp mathematical bold small p
𝐏 \mbfP mbfP mathematical bold capital p
𝛛 \mbfpartial mbfpartial mathematical bold partial differential
𝛟 \mbfphi mbfphi mathematical bold phi symbol
𝚽 \mbfPhi mbfPhi mathematical bold capital phi
𝛑 \mbfpi mbfpi mathematical bold small pi
𝚷 \mbfPi mbfPi mathematical bold capital pi
𝛙 \mbfpsi mbfpsi mathematical bold small psi
𝚿 \mbfPsi mbfPsi mathematical bold capital psi
𝐪 \mbfq mbfq mathematical bold small q
𝐐 \mbfQ mbfQ mathematical bold capital q
𝐫 \mbfr mbfr mathematical bold small r
𝐑 \mbfR mbfR mathematical bold capital r
𝛒 \mbfrho mbfrho mathematical bold small rho
𝚸 \mbfRho mbfRho mathematical bold capital rho
𝐬 \mbfs mbfs mathematical bold small s
𝐒 \mbfS mbfS mathematical bold capital s
𝗮 \mbfsansa mbfsansa mathematical sans-serif bold small a
𝗔 \mbfsansA mbfsansA mathematical sans-serif bold capital a
𝝰 \mbfsansalpha mbfsansalpha mathematical sans-serif bold small alpha
𝝖 \mbfsansAlpha mbfsansAlpha mathematical sans-serif bold capital alpha
𝗯 \mbfsansb mbfsansb mathematical sans-serif bold small b
𝗕 \mbfsansB mbfsansB mathematical sans-serif bold capital b
𝝱 \mbfsansbeta mbfsansbeta mathematical sans-serif bold small beta
𝝗 \mbfsansBeta mbfsansBeta mathematical sans-serif bold capital beta
𝗰 \mbfsansc mbfsansc mathematical sans-serif bold small c
𝗖 \mbfsansC mbfsansC mathematical sans-serif bold capital c
𝞆 \mbfsanschi mbfsanschi mathematical sans-serif bold small chi
𝝬 \mbfsansChi mbfsansChi mathematical sans-serif bold capital chi
𝗱 \mbfsansd mbfsansd mathematical sans-serif bold small d
𝗗 \mbfsansD mbfsansD mathematical sans-serif bold capital d
𝝳 \mbfsansdelta mbfsansdelta mathematical sans-serif bold small delta
𝝙 \mbfsansDelta mbfsansDelta mathematical sans-serif bold capital delta
𝗲 \mbfsanse mbfsanse mathematical sans-serif bold small e
𝗘 \mbfsansE mbfsansE mathematical sans-serif bold capital e
𝟴 \mbfsanseight mbfsanseight mathematical sans-serif bold digit 8
𝞊 \mbfsansepsilon mbfsansepsilon mathematical sans-serif bold varepsilon symbol
𝝚 \mbfsansEpsilon mbfsansEpsilon mathematical sans-serif bold capital epsilon
𝝶 \mbfsanseta mbfsanseta mathematical sans-serif bold small eta
𝝜 \mbfsansEta mbfsansEta mathematical sans-serif bold capital eta
𝗳 \mbfsansf mbfsansf mathematical sans-serif bold small f
𝗙 \mbfsansF mbfsansF mathematical sans-serif bold capital f
𝟱 \mbfsansfive mbfsansfive mathematical sans-serif bold digit 5
𝟰 \mbfsansfour mbfsansfour mathematical sans-serif bold digit 4
𝗴 \mbfsansg mbfsansg mathematical sans-serif bold small g
𝗚 \mbfsansG mbfsansG mathematical sans-serif bold capital g
𝝲 \mbfsansgamma mbfsansgamma mathematical sans-serif bold small gamma
𝝘 \mbfsansGamma mbfsansGamma mathematical sans-serif bold capital gamma
𝗵 \mbfsansh mbfsansh mathematical sans-serif bold small h
𝗛 \mbfsansH mbfsansH mathematical sans-serif bold capital h
𝗶 \mbfsansi mbfsansi mathematical sans-serif bold small i
𝗜 \mbfsansI mbfsansI mathematical sans-serif bold capital i
𝝸 \mbfsansiota mbfsansiota mathematical sans-serif bold small iota
𝝞 \mbfsansIota mbfsansIota mathematical sans-serif bold capital iota
𝗷 \mbfsansj mbfsansj mathematical sans-serif bold small j
𝗝 \mbfsansJ mbfsansJ mathematical sans-serif bold capital j
𝗸 \mbfsansk mbfsansk mathematical sans-serif bold small k
𝗞 \mbfsansK mbfsansK mathematical sans-serif bold capital k
𝝹 \mbfsanskappa mbfsanskappa mathematical sans-serif bold small kappa
𝝟 \mbfsansKappa mbfsansKappa mathematical sans-serif bold capital kappa
𝗹 \mbfsansl mbfsansl mathematical sans-serif bold small l
𝗟 \mbfsansL mbfsansL mathematical sans-serif bold capital l
𝝺 \mbfsanslambda mbfsanslambda mathematical sans-serif bold small lambda
𝝠 \mbfsansLambda mbfsansLambda mathematical sans-serif bold capital lambda
𝗺 \mbfsansm mbfsansm mathematical sans-serif bold small m
𝗠 \mbfsansM mbfsansM mathematical sans-serif bold capital m
𝝻 \mbfsansmu mbfsansmu mathematical sans-serif bold small mu
𝝡 \mbfsansMu mbfsansMu mathematical sans-serif bold capital mu
𝗻 \mbfsansn mbfsansn mathematical sans-serif bold small n
𝗡 \mbfsansN mbfsansN mathematical sans-serif bold capital n
𝝯 \mbfsansnabla mbfsansnabla mathematical sans-serif bold nabla
𝟵 \mbfsansnine mbfsansnine mathematical sans-serif bold digit 9
𝝼 \mbfsansnu mbfsansnu mathematical sans-serif bold small nu
𝝢 \mbfsansNu mbfsansNu mathematical sans-serif bold capital nu
𝗼 \mbfsanso mbfsanso mathematical sans-serif bold small o
𝗢 \mbfsansO mbfsansO mathematical sans-serif bold capital o
𝞈 \mbfsansomega mbfsansomega mathematical sans-serif bold small omega
𝝮 \mbfsansOmega mbfsansOmega mathematical sans-serif bold capital omega
𝝾 \mbfsansomicron mbfsansomicron mathematical sans-serif bold small omicron
𝝤 \mbfsansOmicron mbfsansOmicron mathematical sans-serif bold capital omicron
𝟭 \mbfsansone mbfsansone mathematical sans-serif bold digit 1
𝗽 \mbfsansp mbfsansp mathematical sans-serif bold small p
𝗣 \mbfsansP mbfsansP mathematical sans-serif bold capital p
𝞉 \mbfsanspartial mbfsanspartial mathematical sans-serif bold partial differential
𝞍 \mbfsansphi mbfsansphi mathematical sans-serif bold phi symbol
𝝫 \mbfsansPhi mbfsansPhi mathematical sans-serif bold capital phi
𝝿 \mbfsanspi mbfsanspi mathematical sans-serif bold small pi
𝝥 \mbfsansPi mbfsansPi mathematical sans-serif bold capital pi
𝞇 \mbfsanspsi mbfsanspsi mathematical sans-serif bold small psi
𝝭 \mbfsansPsi mbfsansPsi mathematical sans-serif bold capital psi
𝗾 \mbfsansq mbfsansq mathematical sans-serif bold small q
𝗤 \mbfsansQ mbfsansQ mathematical sans-serif bold capital q
𝗿 \mbfsansr mbfsansr mathematical sans-serif bold small r
𝗥 \mbfsansR mbfsansR mathematical sans-serif bold capital r
𝞀 \mbfsansrho mbfsansrho mathematical sans-serif bold small rho
𝝦 \mbfsansRho mbfsansRho mathematical sans-serif bold capital rho
𝘀 \mbfsanss mbfsanss mathematical sans-serif bold small s
𝗦 \mbfsansS mbfsansS mathematical sans-serif bold capital s
𝟳 \mbfsansseven mbfsansseven mathematical sans-serif bold digit 7
𝞂 \mbfsanssigma mbfsanssigma mathematical sans-serif bold small sigma
𝝨 \mbfsansSigma mbfsansSigma mathematical sans-serif bold capital sigma
𝟲 \mbfsanssix mbfsanssix mathematical sans-serif bold digit 6
𝘁 \mbfsanst mbfsanst mathematical sans-serif bold small t
𝗧 \mbfsansT mbfsansT mathematical sans-serif bold capital t
𝞃 \mbfsanstau mbfsanstau mathematical sans-serif bold small tau
𝝩 \mbfsansTau mbfsansTau mathematical sans-serif bold capital tau
𝝷 \mbfsanstheta mbfsanstheta mathematical sans-serif bold small theta
𝝝 \mbfsansTheta mbfsansTheta mathematical sans-serif bold capital theta
𝟯 \mbfsansthree mbfsansthree mathematical sans-serif bold digit 3
𝟮 \mbfsanstwo mbfsanstwo mathematical sans-serif bold digit 2
𝘂 \mbfsansu mbfsansu mathematical sans-serif bold small u
𝗨 \mbfsansU mbfsansU mathematical sans-serif bold capital u
𝞄 \mbfsansupsilon mbfsansupsilon mathematical sans-serif bold small upsilon
𝝪 \mbfsansUpsilon mbfsansUpsilon mathematical sans-serif bold capital upsilon
𝘃 \mbfsansv mbfsansv mathematical sans-serif bold small v
𝗩 \mbfsansV mbfsansV mathematical sans-serif bold capital v
𝝴 \mbfsansvarepsilon mbfsansvarepsilon mathematical sans-serif bold small varepsilon
𝞌 \mbfsansvarkappa mbfsansvarkappa mathematical sans-serif bold kappa symbol
𝞅 \mbfsansvarphi mbfsansvarphi mathematical sans-serif bold small phi
𝞏 \mbfsansvarpi mbfsansvarpi mathematical sans-serif bold pi symbol
𝞎 \mbfsansvarrho mbfsansvarrho mathematical sans-serif bold rho symbol
𝞁 \mbfsansvarsigma mbfsansvarsigma mathematical sans-serif bold small final sigma
𝞋 \mbfsansvartheta mbfsansvartheta mathematical sans-serif bold theta symbol
𝝧 \mbfsansvarTheta mbfsansvarTheta mathematical sans-serif bold capital theta symbol
𝘄 \mbfsansw mbfsansw mathematical sans-serif bold small w
𝗪 \mbfsansW mbfsansW mathematical sans-serif bold capital w
𝘅 \mbfsansx mbfsansx mathematical sans-serif bold small x
𝗫 \mbfsansX mbfsansX mathematical sans-serif bold capital x
𝝽 \mbfsansxi mbfsansxi mathematical sans-serif bold small xi
𝝣 \mbfsansXi mbfsansXi mathematical sans-serif bold capital xi
𝘆 \mbfsansy mbfsansy mathematical sans-serif bold small y
𝗬 \mbfsansY mbfsansY mathematical sans-serif bold capital y
𝘇 \mbfsansz mbfsansz mathematical sans-serif bold small z
𝗭 \mbfsansZ mbfsansZ mathematical sans-serif bold capital z
𝟬 \mbfsanszero mbfsanszero mathematical sans-serif bold digit 0
𝝵 \mbfsanszeta mbfsanszeta mathematical sans-serif bold small zeta
𝝛 \mbfsansZeta mbfsansZeta mathematical sans-serif bold capital zeta
𝓪 \mbfscra mbfscra mathematical bold script small a
𝓐 \mbfscrA mbfscrA mathematical bold script capital a
𝓫 \mbfscrb mbfscrb mathematical bold script small b
𝓑 \mbfscrB mbfscrB mathematical bold script capital b
𝓬 \mbfscrc mbfscrc mathematical bold script small c
𝓒 \mbfscrC mbfscrC mathematical bold script capital c
𝓭 \mbfscrd mbfscrd mathematical bold script small d
𝓓 \mbfscrD mbfscrD mathematical bold script capital d
𝓮 \mbfscre mbfscre mathematical bold script small e
𝓔 \mbfscrE mbfscrE mathematical bold script capital e
𝓯 \mbfscrf mbfscrf mathematical bold script small f
𝓕 \mbfscrF mbfscrF mathematical bold script capital f
𝓰 \mbfscrg mbfscrg mathematical bold script small g
𝓖 \mbfscrG mbfscrG mathematical bold script capital g
𝓱 \mbfscrh mbfscrh mathematical bold script small h
𝓗 \mbfscrH mbfscrH mathematical bold script capital h
𝓲 \mbfscri mbfscri mathematical bold script small i
𝓘 \mbfscrI mbfscrI mathematical bold script capital i
𝓳 \mbfscrj mbfscrj mathematical bold script small j
𝓙 \mbfscrJ mbfscrJ mathematical bold script capital j
𝓴 \mbfscrk mbfscrk mathematical bold script small k
𝓚 \mbfscrK mbfscrK mathematical bold script capital k
𝓵 \mbfscrl mbfscrl mathematical bold script small l
𝓛 \mbfscrL mbfscrL mathematical bold script capital l
𝓶 \mbfscrm mbfscrm mathematical bold script small m
𝓜 \mbfscrM mbfscrM mathematical bold script capital m
𝓷 \mbfscrn mbfscrn mathematical bold script small n
𝓝 \mbfscrN mbfscrN mathematical bold script capital n
𝓸 \mbfscro mbfscro mathematical bold script small o
𝓞 \mbfscrO mbfscrO mathematical bold script capital o
𝓹 \mbfscrp mbfscrp mathematical bold script small p
𝓟 \mbfscrP mbfscrP mathematical bold script capital p
𝓺 \mbfscrq mbfscrq mathematical bold script small q
𝓠 \mbfscrQ mbfscrQ mathematical bold script capital q
𝓻 \mbfscrr mbfscrr mathematical bold script small r
𝓡 \mbfscrR mbfscrR mathematical bold script capital r
𝓼 \mbfscrs mbfscrs mathematical bold script small s
𝓢 \mbfscrS mbfscrS mathematical bold script capital s
𝓽 \mbfscrt mbfscrt mathematical bold script small t
𝓣 \mbfscrT mbfscrT mathematical bold script capital t
𝓾 \mbfscru mbfscru mathematical bold script small u
𝓤 \mbfscrU mbfscrU mathematical bold script capital u
𝓿 \mbfscrv mbfscrv mathematical bold script small v
𝓥 \mbfscrV mbfscrV mathematical bold script capital v
𝔀 \mbfscrw mbfscrw mathematical bold script small w
𝓦 \mbfscrW mbfscrW mathematical bold script capital w
𝔁 \mbfscrx mbfscrx mathematical bold script small x
𝓧 \mbfscrX mbfscrX mathematical bold script capital x
𝔂 \mbfscry mbfscry mathematical bold script small y
𝓨 \mbfscrY mbfscrY mathematical bold script capital y
𝔃 \mbfscrz mbfscrz mathematical bold script small z
𝓩 \mbfscrZ mbfscrZ mathematical bold script capital z
𝟕 \mbfseven mbfseven mathematical bold digit 7
𝛔 \mbfsigma mbfsigma mathematical bold small sigma
𝚺 \mbfSigma mbfSigma mathematical bold capital sigma
𝟔 \mbfsix mbfsix mathematical bold digit 6
𝐭 \mbft mbft mathematical bold small t
𝐓 \mbfT mbfT mathematical bold capital t
𝛕 \mbftau mbftau mathematical bold small tau
𝚻 \mbfTau mbfTau mathematical bold capital tau
𝛉 \mbftheta mbftheta mathematical bold small theta
𝚯 \mbfTheta mbfTheta mathematical bold capital theta
𝟑 \mbfthree mbfthree mathematical bold digit 3
𝟐 \mbftwo mbftwo mathematical bold digit 2
𝐮 \mbfu mbfu mathematical bold small u
𝐔 \mbfU mbfU mathematical bold capital u
𝛖 \mbfupsilon mbfupsilon mathematical bold small upsilon
𝚼 \mbfUpsilon mbfUpsilon mathematical bold capital upsilon
𝐯 \mbfv mbfv mathematical bold small v
𝐕 \mbfV mbfV mathematical bold capital v
𝛆 \mbfvarepsilon mbfvarepsilon mathematical bold small varepsilon
𝛞 \mbfvarkappa mbfvarkappa mathematical bold kappa symbol
𝛗 \mbfvarphi mbfvarphi mathematical bold small phi
𝛡 \mbfvarpi mbfvarpi mathematical bold pi symbol
𝛠 \mbfvarrho mbfvarrho mathematical bold rho symbol
𝛓 \mbfvarsigma mbfvarsigma mathematical bold small final sigma
𝛝 \mbfvartheta mbfvartheta mathematical bold theta symbol
𝚹 \mbfvarTheta mbfvarTheta mathematical bold capital theta symbol
𝐰 \mbfw mbfw mathematical bold small w
𝐖 \mbfW mbfW mathematical bold capital w
𝐱 \mbfx mbfx mathematical bold small x
𝐗 \mbfX mbfX mathematical bold capital x
𝛏 \mbfxi mbfxi mathematical bold small xi
𝚵 \mbfXi mbfXi mathematical bold capital xi
𝐲 \mbfy mbfy mathematical bold small y
𝐘 \mbfY mbfY mathematical bold capital y
𝐳 \mbfz mbfz mathematical bold small z
𝐙 \mbfZ mbfZ mathematical bold capital z
𝟎 \mbfzero mbfzero mathematical bold digit 0
𝛇 \mbfzeta mbfzeta mathematical bold small zeta
𝚭 \mbfZeta mbfZeta mathematical bold capital zeta
⚫ \mdblkcircle mdblkcircle medium black circle
⬥ \mdblkdiamond mdblkdiamond black medium diamond
⬧ \mdblklozenge mdblklozenge black medium lozenge
◼ \mdblksquare mdblksquare black medium square
● \mdlgblkcircle mdlgblkcircle circle, filled
◆ \mdlgblkdiamond mdlgblkdiamond black diamond
⧫ \mdlgblklozenge mdlgblklozenge black lozenge
■ \mdlgblksquare mdlgblksquare square, filled
○ \mdlgwhtcircle mdlgwhtcircle medium large circle
◇ \mdlgwhtdiamond mdlgwhtdiamond white diamond; diamond, open
◊ \mdlgwhtlozenge mdlgwhtlozenge lozenge or total mark
□ \mdlgwhtsquare mdlgwhtsquare square, open
⦁ \mdsmblkcircle mdsmblkcircle z notation spot
◾ \mdsmblksquare mdsmblksquare black medium small square
⚬ \mdsmwhtcircle mdsmwhtcircle medium small white circle
◽ \mdsmwhtsquare mdsmwhtsquare white medium small square
⚪ \mdwhtcircle mdwhtcircle medium white circle
⬦ \mdwhtdiamond mdwhtdiamond white medium diamond
⬨ \mdwhtlozenge mdwhtlozenge white medium lozenge
◻ \mdwhtsquare mdwhtsquare white medium square
⦯ \measangledltosw measangledltosw measured angle with open arm ending in arrow pointing left and down
⦮ \measangledrtose measangledrtose measured angle with open arm ending in arrow pointing right and down
⦫ \measangleldtosw measangleldtosw measured angle with open arm ending in arrow pointing down and left
⦩ \measanglelutonw measanglelutonw measured angle with open arm ending in arrow pointing up and left
⦪ \measanglerdtose measanglerdtose measured angle with open arm ending in arrow pointing down and right
⦨ \measanglerutone measanglerutone measured angle with open arm ending in arrow pointing up and right
⦭ \measangleultonw measangleultonw measured angle with open arm ending in arrow pointing left and up
⦬ \measangleurtone measangleurtone measured angle with open arm ending in arrow pointing right and up
≞ \measeq measeq measured by (m over equals)
∡ \measuredangle measuredangle angle-measured
⦛ \measuredangleleft measuredangleleft measured angle opening left
⊾ \measuredrightangle measuredrightangle right angle-measured [with arc]
⭑ \medblackstar medblackstar black medium star
⭐ \medwhitestar medwhitestar white medium star
𝔞 \mfraka mfraka mathematical fraktur small a
𝔄 \mfrakA mfrakA mathematical fraktur capital a
𝔟 \mfrakb mfrakb mathematical fraktur small b
𝔅 \mfrakB mfrakB mathematical fraktur capital b
𝔠 \mfrakc mfrakc mathematical fraktur small c
ℭ \mfrakC mfrakC black-letter capital c
𝔡 \mfrakd mfrakd mathematical fraktur small d
𝔇 \mfrakD mfrakD mathematical fraktur capital d
𝔢 \mfrake mfrake mathematical fraktur small e
𝔈 \mfrakE mfrakE mathematical fraktur capital e
𝔣 \mfrakf mfrakf mathematical fraktur small f
𝔉 \mfrakF mfrakF mathematical fraktur capital f
𝔤 \mfrakg mfrakg mathematical fraktur small g
𝔊 \mfrakG mfrakG mathematical fraktur capital g
𝔥 \mfrakh mfrakh mathematical fraktur small h
ℌ \mfrakH mfrakH /frak h, upper case h
𝔦 \mfraki mfraki mathematical fraktur small i
𝔧 \mfrakj mfrakj mathematical fraktur small j
𝔍 \mfrakJ mfrakJ mathematical fraktur capital j
𝔨 \mfrakk mfrakk mathematical fraktur small k
𝔎 \mfrakK mfrakK mathematical fraktur capital k
𝔩 \mfrakl mfrakl mathematical fraktur small l
𝔏 \mfrakL mfrakL mathematical fraktur capital l
𝔪 \mfrakm mfrakm mathematical fraktur small m
𝔐 \mfrakM mfrakM mathematical fraktur capital m
𝔫 \mfrakn mfrakn mathematical fraktur small n
𝔑 \mfrakN mfrakN mathematical fraktur capital n
𝔬 \mfrako mfrako mathematical fraktur small o
𝔒 \mfrakO mfrakO mathematical fraktur capital o
𝔭 \mfrakp mfrakp mathematical fraktur small p
𝔓 \mfrakP mfrakP mathematical fraktur capital p
𝔮 \mfrakq mfrakq mathematical fraktur small q
𝔔 \mfrakQ mfrakQ mathematical fraktur capital q
𝔯 \mfrakr mfrakr mathematical fraktur small r
𝔰 \mfraks mfraks mathematical fraktur small s
𝔖 \mfrakS mfrakS mathematical fraktur capital s
𝔱 \mfrakt mfrakt mathematical fraktur small t
𝔗 \mfrakT mfrakT mathematical fraktur capital t
𝔲 \mfraku mfraku mathematical fraktur small u
𝔘 \mfrakU mfrakU mathematical fraktur capital u
𝔳 \mfrakv mfrakv mathematical fraktur small v
𝔙 \mfrakV mfrakV mathematical fraktur capital v
𝔴 \mfrakw mfrakw mathematical fraktur small w
𝔚 \mfrakW mfrakW mathematical fraktur capital w
𝔵 \mfrakx mfrakx mathematical fraktur small x
𝔛 \mfrakX mfrakX mathematical fraktur capital x
𝔶 \mfraky mfraky mathematical fraktur small y
𝔜 \mfrakY mfrakY mathematical fraktur capital y
𝔷 \mfrakz mfrakz mathematical fraktur small z
ℨ \mfrakZ mfrakZ /frak z, upper case z
℧ \mho mho conductance
∣ \mid mid /mid r:
⩝ \midbarvee midbarvee logical or with horizontal dash
⩜ \midbarwedge midbarwedge ogical and with horizontal dash
⫰ \midcir midcir vertical line with circle below
− \minus minus minus sign
⨪ \minusdot minusdot minus sign with dot below
⨫ \minusfdots minusfdots minus sign with falling dots
⨬ \minusrdots minusrdots minus sign with rising dots
𝑎 \mita mita mathematical italic small a
𝐴 \mitA mitA mathematical italic capital a
𝛼 \mitalpha mitalpha mathematical italic small alpha
𝛢 \mitAlpha mitAlpha mathematical italic capital alpha
𝑏 \mitb mitb mathematical italic small b
𝐵 \mitB mitB mathematical italic capital b
ⅆ \mitBbbd mitBbbd double-struck italic small d
ⅅ \mitBbbD mitBbbD double-struck italic capital d
ⅇ \mitBbbe mitBbbe double-struck italic small e
ⅈ \mitBbbi mitBbbi double-struck italic small i
ⅉ \mitBbbj mitBbbj double-struck italic small j
𝛽 \mitbeta mitbeta mathematical italic small beta
𝛣 \mitBeta mitBeta mathematical italic capital beta
𝑐 \mitc mitc mathematical italic small c
𝐶 \mitC mitC mathematical italic capital c
𝜒 \mitchi mitchi mathematical italic small chi
𝛸 \mitChi mitChi mathematical italic capital chi
𝑑 \mitd mitd mathematical italic small d
𝐷 \mitD mitD mathematical italic capital d
𝛿 \mitdelta mitdelta mathematical italic small delta
𝛥 \mitDelta mitDelta mathematical italic capital delta
𝑒 \mite mite mathematical italic small e
𝐸 \mitE mitE mathematical italic capital e
𝜖 \mitepsilon mitepsilon mathematical italic varepsilon symbol
𝛦 \mitEpsilon mitEpsilon mathematical italic capital epsilon
𝜂 \miteta miteta mathematical italic small eta
𝛨 \mitEta mitEta mathematical italic capital eta
𝑓 \mitf mitf mathematical italic small f
𝐹 \mitF mitF mathematical italic capital f
𝑔 \mitg mitg mathematical italic small g
𝐺 \mitG mitG mathematical italic capital g
𝛾 \mitgamma mitgamma mathematical italic small gamma
𝛤 \mitGamma mitGamma mathematical italic capital gamma
𝐻 \mitH mitH mathematical italic capital h
𝑖 \miti miti mathematical italic small i
𝐼 \mitI mitI mathematical italic capital i
𝜄 \mitiota mitiota mathematical italic small iota
𝛪 \mitIota mitIota mathematical italic capital iota
𝑗 \mitj mitj mathematical italic small j
𝐽 \mitJ mitJ mathematical italic capital j
𝑘 \mitk mitk mathematical italic small k
𝐾 \mitK mitK mathematical italic capital k
𝜅 \mitkappa mitkappa mathematical italic small kappa
𝛫 \mitKappa mitKappa mathematical italic capital kappa
𝑙 \mitl mitl mathematical italic small l
𝐿 \mitL mitL mathematical italic capital l
𝜆 \mitlambda mitlambda mathematical italic small lambda
𝛬 \mitLambda mitLambda mathematical italic capital lambda
𝑚 \mitm mitm mathematical italic small m
𝑀 \mitM mitM mathematical italic capital m
𝜇 \mitmu mitmu mathematical italic small mu
𝛭 \mitMu mitMu mathematical italic capital mu
𝑛 \mitn mitn mathematical italic small n
𝑁 \mitN mitN mathematical italic capital n
𝛻 \mitnabla mitnabla mathematical italic nabla
𝜈 \mitnu mitnu mathematical italic small nu
𝛮 \mitNu mitNu mathematical italic capital nu
𝑜 \mito mito mathematical italic small o
𝑂 \mitO mitO mathematical italic capital o
𝜔 \mitomega mitomega mathematical italic small omega
𝛺 \mitOmega mitOmega mathematical italic capital omega
𝜊 \mitomicron mitomicron mathematical italic small omicron
𝛰 \mitOmicron mitOmicron mathematical italic capital omicron
𝑝 \mitp mitp mathematical italic small p
𝑃 \mitP mitP mathematical italic capital p
𝜕 \mitpartial mitpartial mathematical italic partial differential
𝜙 \mitphi mitphi mathematical italic phi symbol
𝛷 \mitPhi mitPhi mathematical italic capital phi
𝜋 \mitpi mitpi mathematical italic small pi
𝛱 \mitPi mitPi mathematical italic capital pi
𝜓 \mitpsi mitpsi mathematical italic small psi
𝛹 \mitPsi mitPsi mathematical italic capital psi
𝑞 \mitq mitq mathematical italic small q
𝑄 \mitQ mitQ mathematical italic capital q
𝑟 \mitr mitr mathematical italic small r
𝑅 \mitR mitR mathematical italic capital r
𝜌 \mitrho mitrho mathematical italic small rho
𝛲 \mitRho mitRho mathematical italic capital rho
𝑠 \mits mits mathematical italic small s
𝑆 \mitS mitS mathematical italic capital s
𝘢 \mitsansa mitsansa mathematical sans-serif italic small a
𝘈 \mitsansA mitsansA mathematical sans-serif italic capital a
𝘣 \mitsansb mitsansb mathematical sans-serif italic small b
𝘉 \mitsansB mitsansB mathematical sans-serif italic capital b
𝘤 \mitsansc mitsansc mathematical sans-serif italic small c
𝘊 \mitsansC mitsansC mathematical sans-serif italic capital c
𝘥 \mitsansd mitsansd mathematical sans-serif italic small d
𝘋 \mitsansD mitsansD mathematical sans-serif italic capital d
𝘦 \mitsanse mitsanse mathematical sans-serif italic small e
𝘌 \mitsansE mitsansE mathematical sans-serif italic capital e
𝘧 \mitsansf mitsansf mathematical sans-serif italic small f
𝘍 \mitsansF mitsansF mathematical sans-serif italic capital f
𝘨 \mitsansg mitsansg mathematical sans-serif italic small g
𝘎 \mitsansG mitsansG mathematical sans-serif italic capital g
𝘩 \mitsansh mitsansh mathematical sans-serif italic small h
𝘏 \mitsansH mitsansH mathematical sans-serif italic capital h
𝘪 \mitsansi mitsansi mathematical sans-serif italic small i
𝘐 \mitsansI mitsansI mathematical sans-serif italic capital i
𝘫 \mitsansj mitsansj mathematical sans-serif italic small j
𝘑 \mitsansJ mitsansJ mathematical sans-serif italic capital j
𝘬 \mitsansk mitsansk mathematical sans-serif italic small k
𝘒 \mitsansK mitsansK mathematical sans-serif italic capital k
𝘭 \mitsansl mitsansl mathematical sans-serif italic small l
𝘓 \mitsansL mitsansL mathematical sans-serif italic capital l
𝘮 \mitsansm mitsansm mathematical sans-serif italic small m
𝘔 \mitsansM mitsansM mathematical sans-serif italic capital m
𝘯 \mitsansn mitsansn mathematical sans-serif italic small n
𝘕 \mitsansN mitsansN mathematical sans-serif italic capital n
𝘰 \mitsanso mitsanso mathematical sans-serif italic small o
𝘖 \mitsansO mitsansO mathematical sans-serif italic capital o
𝘱 \mitsansp mitsansp mathematical sans-serif italic small p
𝘗 \mitsansP mitsansP mathematical sans-serif italic capital p
𝘲 \mitsansq mitsansq mathematical sans-serif italic small q
𝘘 \mitsansQ mitsansQ mathematical sans-serif italic capital q
𝘳 \mitsansr mitsansr mathematical sans-serif italic small r
𝘙 \mitsansR mitsansR mathematical sans-serif italic capital r
𝘴 \mitsanss mitsanss mathematical sans-serif italic small s
𝘚 \mitsansS mitsansS mathematical sans-serif italic capital s
𝘵 \mitsanst mitsanst mathematical sans-serif italic small t
𝘛 \mitsansT mitsansT mathematical sans-serif italic capital t
𝘶 \mitsansu mitsansu mathematical sans-serif italic small u
𝘜 \mitsansU mitsansU mathematical sans-serif italic capital u
𝘷 \mitsansv mitsansv mathematical sans-serif italic small v
𝘝 \mitsansV mitsansV mathematical sans-serif italic capital v
𝘸 \mitsansw mitsansw mathematical sans-serif italic small w
𝘞 \mitsansW mitsansW mathematical sans-serif italic capital w
𝘹 \mitsansx mitsansx mathematical sans-serif italic small x
𝘟 \mitsansX mitsansX mathematical sans-serif italic capital x
𝘺 \mitsansy mitsansy mathematical sans-serif italic small y
𝘠 \mitsansY mitsansY mathematical sans-serif italic capital y
𝘻 \mitsansz mitsansz mathematical sans-serif italic small z
𝘡 \mitsansZ mitsansZ mathematical sans-serif italic capital z
𝜎 \mitsigma mitsigma mathematical italic small sigma
𝛴 \mitSigma mitSigma mathematical italic capital sigma
𝑡 \mitt mitt mathematical italic small t
𝑇 \mitT mitT mathematical italic capital t
𝜏 \mittau mittau mathematical italic small tau
𝛵 \mitTau mitTau mathematical italic capital tau
𝜃 \mittheta mittheta mathematical italic small theta
𝛩 \mitTheta mitTheta mathematical italic capital theta
𝑢 \mitu mitu mathematical italic small u
𝑈 \mitU mitU mathematical italic capital u
𝜐 \mitupsilon mitupsilon mathematical italic small upsilon
𝛶 \mitUpsilon mitUpsilon mathematical italic capital upsilon
𝑣 \mitv mitv mathematical italic small v
𝑉 \mitV mitV mathematical italic capital v
𝜀 \mitvarepsilon mitvarepsilon mathematical italic small varepsilon
𝜘 \mitvarkappa mitvarkappa mathematical italic kappa symbol
𝜑 \mitvarphi mitvarphi mathematical italic small phi
𝜛 \mitvarpi mitvarpi mathematical italic pi symbol
𝜚 \mitvarrho mitvarrho mathematical italic rho symbol
𝜍 \mitvarsigma mitvarsigma mathematical italic small final sigma
𝜗 \mitvartheta mitvartheta mathematical italic theta symbol
𝛳 \mitvarTheta mitvarTheta mathematical italic capital theta symbol
𝑤 \mitw mitw mathematical italic small w
𝑊 \mitW mitW mathematical italic capital w
𝑥 \mitx mitx mathematical italic small x
𝑋 \mitX mitX mathematical italic capital x
𝜉 \mitxi mitxi mathematical italic small xi
𝛯 \mitXi mitXi mathematical italic capital xi
𝑦 \mity mity mathematical italic small y
𝑌 \mitY mitY mathematical italic capital y
𝑧 \mitz mitz mathematical italic small z
𝑍 \mitZ mitZ mathematical italic capital z
𝜁 \mitzeta mitzeta mathematical italic small zeta
𝛧 \mitZeta mitZeta mathematical italic capital zeta
⫛ \mlcp mlcp transversal intersection
⊧ \models models models (vertical, short double dash)
⨊ \modtwosum modtwosum modulo two sum
∓ \mp mp minus-or-plus sign
𝖺 \msansa msansa mathematical sans-serif small a
𝖠 \msansA msansA mathematical sans-serif capital a
𝖻 \msansb msansb mathematical sans-serif small b
𝖡 \msansB msansB mathematical sans-serif capital b
𝖼 \msansc msansc mathematical sans-serif small c
𝖢 \msansC msansC mathematical sans-serif capital c
𝖽 \msansd msansd mathematical sans-serif small d
𝖣 \msansD msansD mathematical sans-serif capital d
𝖾 \msanse msanse mathematical sans-serif small e
𝖤 \msansE msansE mathematical sans-serif capital e
𝟪 \msanseight msanseight mathematical sans-serif digit 8
𝖿 \msansf msansf mathematical sans-serif small f
𝖥 \msansF msansF mathematical sans-serif capital f
𝟧 \msansfive msansfive mathematical sans-serif digit 5
𝟦 \msansfour msansfour mathematical sans-serif digit 4
𝗀 \msansg msansg mathematical sans-serif small g
𝖦 \msansG msansG mathematical sans-serif capital g
𝗁 \msansh msansh mathematical sans-serif small h
𝖧 \msansH msansH mathematical sans-serif capital h
𝗂 \msansi msansi mathematical sans-serif small i
𝖨 \msansI msansI mathematical sans-serif capital i
𝗃 \msansj msansj mathematical sans-serif small j
𝖩 \msansJ msansJ mathematical sans-serif capital j
𝗄 \msansk msansk mathematical sans-serif small k
𝖪 \msansK msansK mathematical sans-serif capital k
𝗅 \msansl msansl mathematical sans-serif small l
𝖫 \msansL msansL mathematical sans-serif capital l
𝗆 \msansm msansm mathematical sans-serif small m
𝖬 \msansM msansM mathematical sans-serif capital m
𝗇 \msansn msansn mathematical sans-serif small n
𝖭 \msansN msansN mathematical sans-serif capital n
𝟫 \msansnine msansnine mathematical sans-serif digit 9
𝗈 \msanso msanso mathematical sans-serif small o
𝖮 \msansO msansO mathematical sans-serif capital o
𝟣 \msansone msansone mathematical sans-serif digit 1
𝗉 \msansp msansp mathematical sans-serif small p
𝖯 \msansP msansP mathematical sans-serif capital p
𝗊 \msansq msansq mathematical sans-serif small q
𝖰 \msansQ msansQ mathematical sans-serif capital q
𝗋 \msansr msansr mathematical sans-serif small r
𝖱 \msansR msansR mathematical sans-serif capital r
𝗌 \msanss msanss mathematical sans-serif small s
𝖲 \msansS msansS mathematical sans-serif capital s
𝟩 \msansseven msansseven mathematical sans-serif digit 7
𝟨 \msanssix msanssix mathematical sans-serif digit 6
𝗍 \msanst msanst mathematical sans-serif small t
𝖳 \msansT msansT mathematical sans-serif capital t
𝟥 \msansthree msansthree mathematical sans-serif digit 3
𝟤 \msanstwo msanstwo mathematical sans-serif digit 2
𝗎 \msansu msansu mathematical sans-serif small u
𝖴 \msansU msansU mathematical sans-serif capital u
𝗏 \msansv msansv mathematical sans-serif small v
𝖵 \msansV msansV mathematical sans-serif capital v
𝗐 \msansw msansw mathematical sans-serif small w
𝖶 \msansW msansW mathematical sans-serif capital w
𝗑 \msansx msansx mathematical sans-serif small x
𝖷 \msansX msansX mathematical sans-serif capital x
𝗒 \msansy msansy mathematical sans-serif small y
𝖸 \msansY msansY mathematical sans-serif capital y
𝗓 \msansz msansz mathematical sans-serif small z
𝖹 \msansZ msansZ mathematical sans-serif capital z
𝟢 \msanszero msanszero mathematical sans-serif digit 0
𝒶 \mscra mscra mathematical script small a
𝒜 \mscrA mscrA mathematical script capital a
𝒷 \mscrb mscrb mathematical script small b
ℬ \mscrB mscrB bernoulli function (script capital b)
𝒸 \mscrc mscrc mathematical script small c
𝒞 \mscrC mscrC mathematical script capital c
𝒹 \mscrd mscrd mathematical script small d
𝒟 \mscrD mscrD mathematical script capital d
ℯ \mscre mscre /scr e, script letter e
ℰ \mscrE mscrE /scr e, script letter e
𝒻 \mscrf mscrf mathematical script small f
ℱ \mscrF mscrF /scr f, script letter f
ℊ \mscrg mscrg /scr g, script letter g
𝒢 \mscrG mscrG mathematical script capital g
𝒽 \mscrh mscrh mathematical script small h
ℋ \mscrH mscrH hamiltonian (script capital h)
𝒾 \mscri mscri mathematical script small i
ℐ \mscrI mscrI /scr i, script letter i
𝒿 \mscrj mscrj mathematical script small j
𝒥 \mscrJ mscrJ mathematical script capital j
𝓀 \mscrk mscrk mathematical script small k
𝒦 \mscrK mscrK mathematical script capital k
𝓁 \mscrl mscrl mathematical script small l
ℒ \mscrL mscrL lagrangian (script capital l)
𝓂 \mscrm mscrm mathematical script small m
ℳ \mscrM mscrM physics m-matrix (script capital m)
𝓃 \mscrn mscrn mathematical script small n
𝒩 \mscrN mscrN mathematical script capital n
ℴ \mscro mscro order of (script small o)
𝒪 \mscrO mscrO mathematical script capital o
𝓅 \mscrp mscrp mathematical script small p
𝒫 \mscrP mscrP mathematical script capital p
𝓆 \mscrq mscrq mathematical script small q
𝒬 \mscrQ mscrQ mathematical script capital q
𝓇 \mscrr mscrr mathematical script small r
ℛ \mscrR mscrR /scr r, script letter r
𝓈 \mscrs mscrs mathematical script small s
𝒮 \mscrS mscrS mathematical script capital s
𝓉 \mscrt mscrt mathematical script small t
𝒯 \mscrT mscrT mathematical script capital t
𝓊 \mscru mscru mathematical script small u
𝒰 \mscrU mscrU mathematical script capital u
𝓋 \mscrv mscrv mathematical script small v
𝒱 \mscrV mscrV mathematical script capital v
𝓌 \mscrw mscrw mathematical script small w
𝒲 \mscrW mscrW mathematical script capital w
𝓍 \mscrx mscrx mathematical script small x
𝒳 \mscrX mscrX mathematical script capital x
𝓎 \mscry mscry mathematical script small y
𝒴 \mscrY mscrY mathematical script capital y
𝓏 \mscrz mscrz mathematical script small z
𝒵 \mscrZ mscrZ mathematical script capital z
𝚊 \mtta mtta mathematical monospace small a
𝙰 \mttA mttA mathematical monospace capital a
𝚋 \mttb mttb mathematical monospace small b
𝙱 \mttB mttB mathematical monospace capital b
𝚌 \mttc mttc mathematical monospace small c
𝙲 \mttC mttC mathematical monospace capital c
𝚍 \mttd mttd mathematical monospace small d
𝙳 \mttD mttD mathematical monospace capital d
𝚎 \mtte mtte mathematical monospace small e
𝙴 \mttE mttE mathematical monospace capital e
𝟾 \mtteight mtteight mathematical monospace digit 8
𝚏 \mttf mttf mathematical monospace small f
𝙵 \mttF mttF mathematical monospace capital f
𝟻 \mttfive mttfive mathematical monospace digit 5
𝟺 \mttfour mttfour mathematical monospace digit 4
𝚐 \mttg mttg mathematical monospace small g
𝙶 \mttG mttG mathematical monospace capital g
𝚑 \mtth mtth mathematical monospace small h
𝙷 \mttH mttH mathematical monospace capital h
𝚒 \mtti mtti mathematical monospace small i
𝙸 \mttI mttI mathematical monospace capital i
𝚓 \mttj mttj mathematical monospace small j
𝙹 \mttJ mttJ mathematical monospace capital j
𝚔 \mttk mttk mathematical monospace small k
𝙺 \mttK mttK mathematical monospace capital k
𝚕 \mttl mttl mathematical monospace small l
𝙻 \mttL mttL mathematical monospace capital l
𝚖 \mttm mttm mathematical monospace small m
𝙼 \mttM mttM mathematical monospace capital m
𝚗 \mttn mttn mathematical monospace small n
𝙽 \mttN mttN mathematical monospace capital n
𝟿 \mttnine mttnine mathematical monospace digit 9
𝚘 \mtto mtto mathematical monospace small o
𝙾 \mttO mttO mathematical monospace capital o
𝟷 \mttone mttone mathematical monospace digit 1
𝚙 \mttp mttp mathematical monospace small p
𝙿 \mttP mttP mathematical monospace capital p
𝚚 \mttq mttq mathematical monospace small q
𝚀 \mttQ mttQ mathematical monospace capital q
𝚛 \mttr mttr mathematical monospace small r
𝚁 \mttR mttR mathematical monospace capital r
𝚜 \mtts mtts mathematical monospace small s
𝚂 \mttS mttS mathematical monospace capital s
𝟽 \mttseven mttseven mathematical monospace digit 7
𝟼 \mttsix mttsix mathematical monospace digit 6
𝚝 \mttt mttt mathematical monospace small t
𝚃 \mttT mttT mathematical monospace capital t
𝟹 \mttthree mttthree mathematical monospace digit 3
𝟸 \mtttwo mtttwo mathematical monospace digit 2
𝚞 \mttu mttu mathematical monospace small u
𝚄 \mttU mttU mathematical monospace capital u
𝚟 \mttv mttv mathematical monospace small v
𝚅 \mttV mttV mathematical monospace capital v
𝚠 \mttw mttw mathematical monospace small w
𝚆 \mttW mttW mathematical monospace capital w
𝚡 \mttx mttx mathematical monospace small x
𝚇 \mttX mttX mathematical monospace capital x
𝚢 \mtty mtty mathematical monospace small y
𝚈 \mttY mttY mathematical monospace capital y
𝚣 \mttz mttz mathematical monospace small z
𝚉 \mttZ mttZ mathematical monospace capital z
𝟶 \mttzero mttzero mathematical monospace digit 0
⊸ \multimap multimap /multimap a:
⟜ \multimapinv multimapinv left multimap
α \mupalpha mupalpha small alpha, greek
Α \mupAlpha mupAlpha capital alpha, greek
β \mupbeta mupbeta small beta, greek
Β \mupBeta mupBeta capital beta, greek
χ \mupchi mupchi small chi, greek
Χ \mupChi mupChi capital chi, greek
δ \mupdelta mupdelta small delta, greek
Δ \mupDelta mupDelta capital delta, greek
ϵ \mupepsilon mupepsilon greek lunate varepsilon symbol
Ε \mupEpsilon mupEpsilon capital epsilon, greek
η \mupeta mupeta small eta, greek
Η \mupEta mupEta capital eta, greek
γ \mupgamma mupgamma small gamma, greek
Γ \mupGamma mupGamma capital gamma, greek
ι \mupiota mupiota small iota, greek
Ι \mupIota mupIota capital iota, greek
κ \mupkappa mupkappa small kappa, greek
Κ \mupKappa mupKappa capital kappa, greek
λ \muplambda muplambda small lambda, greek
Λ \mupLambda mupLambda capital lambda, greek
μ \mupmu mupmu small mu, greek
Μ \mupMu mupMu capital mu, greek
ν \mupnu mupnu small nu, greek
Ν \mupNu mupNu capital nu, greek
ω \mupomega mupomega small omega, greek
Ω \mupOmega mupOmega capital omega, greek
ο \mupomicron mupomicron small omicron, greek
Ο \mupOmicron mupOmicron capital omicron, greek
ϕ \mupphi mupphi /straightphi - small phi, greek
Φ \mupPhi mupPhi capital phi, greek
π \muppi muppi small pi, greek
Π \mupPi mupPi capital pi, greek
ψ \muppsi muppsi small psi, greek
Ψ \mupPsi mupPsi capital psi, greek
ρ \muprho muprho small rho, greek
Ρ \mupRho mupRho capital rho, greek
σ \mupsigma mupsigma small sigma, greek
Σ \mupSigma mupSigma capital sigma, greek
τ \muptau muptau small tau, greek
Τ \mupTau mupTau capital tau, greek
θ \muptheta muptheta straight theta, small theta, greek
Θ \mupTheta mupTheta capital theta, greek
υ \mupupsilon mupupsilon small upsilon, greek
Υ \mupUpsilon mupUpsilon capital upsilon, greek
ε \mupvarepsilon mupvarepsilon rounded small varepsilon, greek
ϰ \mupvarkappa mupvarkappa rounded small kappa, greek
φ \mupvarphi mupvarphi curly or open small phi, greek
ϖ \mupvarpi mupvarpi rounded small pi (pomega), greek
ϱ \mupvarrho mupvarrho rounded small rho, greek
ς \mupvarsigma mupvarsigma terminal sigma, greek
ϑ \mupvartheta mupvartheta /vartheta - curly or open theta
ϴ \mupvarTheta mupvarTheta greek capital theta symbol
ξ \mupxi mupxi small xi, greek
Ξ \mupXi mupXi capital xi, greek
ζ \mupzeta mupzeta small zeta, greek
Ζ \mupZeta mupZeta capital zeta, greek
∇ \nabla nabla nabla, del, hamilton operator
≉ \napprox napprox not approximate
≭ \nasymp nasymp not asymptotically equal to
♮ \natural natural music natural
≇ \ncong ncong not congruent with
≠ \ne ne /ne /neq r: not equal
↗ \nearrow nearrow ne pointing arrow
⇗ \Nearrow Nearrow ne pointing double arrow
¬ \neg neg /neg /lnot not sign
⤱ \neovnwarrow neovnwarrow north east arrow crossing north west arrow
⤮ \neovsearrow neovsearrow north east arrow crossing south east arrow
≢ \nequiv nequiv not identical with
⤢ \neswarrow neswarrow north east and south west arrow
⚲ \neuter neuter neuter
∄ \nexists nexists negated exists
≱ \ngeq ngeq not greater-than-or-equal
≯ \ngtr ngtr not greater-than
≹ \ngtrless ngtrless not greater, less
≵ \ngtrsim ngtrsim not greater, similar
⇟ \nHdownarrow nHdownarrow downwards arrow with double stroke
⫲ \nhpar nhpar parallel with horizontal stroke
⇞ \nHuparrow nHuparrow upwards arrow with double stroke
⫵ \nhVvert nhVvert triple vertical bar with horizontal stroke
∋ \ni ni contains, variant
⋾ \niobar niobar small contains with overbar
⋼ \nis nis small contains with vertical bar at end of horizontal stroke
⋺ \nisd nisd contains with long horizontal stroke
↚ \nleftarrow nleftarrow not left arrow
⇍ \nLeftarrow nLeftarrow not implied by
↮ \nleftrightarrow nleftrightarrow not left and right arrow
⇎ \nLeftrightarrow nLeftrightarrow not left and right double arrows
≰ \nleq nleq not less-than-or-equal
≮ \nless nless not less-than
≸ \nlessgtr nlessgtr not less, greater
≴ \nlesssim nlesssim not less, similar
∤ \nmid nmid negated mid
∌ \nni nni negated contains, variant
⫬ \Not Not double stroke not sign
̸ \notaccent notaccent combining long solidus overlay
∉ \notin notin negated set membership
∦ \nparallel nparallel not parallel
⨔ \npolint npolint line integration not including the pole
⊀ \nprec nprec not precedes
⋠ \npreccurlyeq npreccurlyeq not precedes, curly equals
↛ \nrightarrow nrightarrow not right arrow
⇏ \nRightarrow nRightarrow not implies
≁ \nsim nsim not similar
≄ \nsime nsime not similar, equals
≄ \nsimeq nsimeq not similar, equals (alias)
⋢ \nsqsubseteq nsqsubseteq not, square subset, equals
⋣ \nsqsupseteq nsqsupseteq not, square superset, equals
⊄ \nsubset nsubset not subset, variant [slash negation]
⊈ \nsubseteq nsubseteq not subset, equals
⊁ \nsucc nsucc not succeeds
⋡ \nsucccurlyeq nsucccurlyeq not succeeds, curly equals
⊅ \nsupset nsupset not superset, variant [slash negation]
⊉ \nsupseteq nsupseteq not superset, equals
⋬ \ntrianglelefteq ntrianglelefteq not left triangle, equals
⋭ \ntrianglerighteq ntrianglerighteq not right triangle, equals
⋪ \nvartriangleleft nvartriangleleft not left triangle
⋫ \nvartriangleright nvartriangleright not right triangle
⊬ \nvdash nvdash not vertical, dash
⊭ \nvDash nvDash not vertical, double dash
⊮ \nVdash nVdash not double vertical, dash
⊯ \nVDash nVDash not double vert, double dash
⧞ \nvinfty nvinfty infinity negated with vertical bar
⇷ \nvleftarrow nvleftarrow leftwards arrow with vertical stroke
⤂ \nvLeftarrow nvLeftarrow leftwards double arrow with vertical stroke
⇺ \nVleftarrow nVleftarrow leftwards arrow with double vertical stroke
⬹ \nvleftarrowtail nvleftarrowtail leftwards arrow with tail with vertical stroke
⬺ \nVleftarrowtail nVleftarrowtail leftwards arrow with tail with double vertical stroke
⇹ \nvleftrightarrow nvleftrightarrow left right arrow with vertical stroke
⤄ \nvLeftrightarrow nvLeftrightarrow left right double arrow with vertical stroke
⇼ \nVleftrightarrow nVleftrightarrow left right arrow with double vertical stroke
⇸ \nvrightarrow nvrightarrow rightwards arrow with vertical stroke
⤃ \nvRightarrow nvRightarrow rightwards double arrow with vertical stroke
⇻ \nVrightarrow nVrightarrow rightwards arrow with double vertical stroke
⤔ \nvrightarrowtail nvrightarrowtail rightwards arrow with tail with vertical stroke
⤕ \nVrightarrowtail nVrightarrowtail rightwards arrow with tail with double vertical stroke
⬴ \nvtwoheadleftarrow nvtwoheadleftarrow leftwards two-headed arrow with vertical stroke
⬵ \nVtwoheadleftarrow nVtwoheadleftarrow leftwards two-headed arrow with double vertical stroke
⬼ \nvtwoheadleftarrowtail nvtwoheadleftarrowtail leftwards two-headed arrow with tail with vertical stroke
⬽ \nVtwoheadleftarrowtail nVtwoheadleftarrowtail leftwards two-headed arrow with tail with double vertical stroke
⤀ \nvtwoheadrightarrow nvtwoheadrightarrow rightwards two-headed arrow with vertical stroke
⤁ \nVtwoheadrightarrow nVtwoheadrightarrow rightwards two-headed arrow with double vertical stroke
⤗ \nvtwoheadrightarrowtail nvtwoheadrightarrowtail rightwards two-headed arrow with tail with vertical stroke
⤘ \nVtwoheadrightarrowtail nVtwoheadrightarrowtail rightwards two-headed arrow with tail with double vertical stroke
↖ \nwarrow nwarrow nw pointing arrow
⇖ \Nwarrow Nwarrow nw pointing double arrow
⤲ \nwovnearrow nwovnearrow north west arrow crossing north east arrow
⤡ \nwsearrow nwsearrow north west and south east arrow
⌽ \obar obar circle with vertical bar
⦺ \obot obot circle divided by horizontal bar and top half divided by vertical bar
⏠ \obrbrak obrbrak top tortoise shell bracket (mathematical use)
⦸ \obslash obslash circled reverse solidus
̊ \ocirc ocirc ring
̕ \ocommatopright ocommatopright combining comma above right
⨸ \odiv odiv circled division sign
⊙ \odot odot middle dot in circle
⦼ \odotslashdot odotslashdot circled anticlockwise-rotated division sign
⧁ \ogreaterthan ogreaterthan circled greater-than
∰ \oiiint oiiint triple contour integral operator
∯ \oiint oiint double contour integral operator
∮ \oint oint contour integral operator
∳ \ointctrclockwise ointctrclockwise contour integral, anticlockwise
⦻ \olcross olcross circle with superimposed x
⧀ \olessthan olessthan circled less-than
⊖ \ominus ominus minus sign in circle
⦹ \operp operp circled perpendicular
⊕ \oplus oplus plus sign in circle
⨭ \opluslhrim opluslhrim plus sign in left half circle
⨮ \oplusrhrim oplusrhrim plus sign in right half circle
⊶ \origof origof original of
⊘ \oslash oslash solidus in circle
⊗ \otimes otimes multiply sign in circle
⨷ \Otimes Otimes multiplication sign in double circle
⨶ \otimeshat otimeshat circled multiplication sign with circumflex accent
⨴ \otimeslhrim otimeslhrim multiplication sign in left half circle
⨵ \otimesrhrim otimesrhrim multiplication sign in right half circle
̒ \oturnedcomma oturnedcomma combining turned comma above
̅ \overbar overbar overbar embellishment
⏞ \overbrace overbrace top curly bracket (mathematical use)
⎴ \overbracket overbracket top square bracket
⃖ \overleftarrow overleftarrow combining left arrow above
⃐ \overleftharpoon overleftharpoon combining left harpoon above
⃡ \overleftrightarrow overleftrightarrow combining left right arrow above
⏜ \overparen overparen top parenthesis (mathematical use)
⃗ \overrightarrow overrightarrow combining left arrow above
⃑ \overrightharpoon overrightharpoon combining right harpoon above
̉ \ovhook ovhook combining hook above
∥ \parallel parallel parallel
▱ \parallelogram parallelogram parallelogram, open
▰ \parallelogramblack parallelogramblack black parallelogram
⫳ \parsim parsim parallel with tilde operator
∂ \partial partial partial differential
⪣ \partialmeetcontraction partialmeetcontraction double less-than with underbar
⬠ \pentagon pentagon white pentagon
⬟ \pentagonblack pentagonblack black pentagon
⟂ \perp perp perpendicular
⫡ \perps perps perpendicular with s
⋔ \pitchfork pitchfork pitchfork
ℎ \Planckconst Planckconst planck constant
⨥ \plusdot plusdot plus sign with dot below
⩲ \pluseqq pluseqq plus sign above equals sign
⨣ \plushat plushat plus sign with circumflex accent above
⨦ \plussim plussim plus sign with tilde below
⨧ \plussubtwo plussubtwo plus sign with subscript two
⨨ \plustrif plustrif plus sign with black triangle
± \pm pm plus-or-minus sign
⨕ \pointint pointint integral around a point operator
〒 \postalmark postalmark postal mark
≺ \prec prec precedes
⪻ \Prec Prec double precedes
⪷ \precapprox precapprox precedes above almost equal to
≼ \preccurlyeq preccurlyeq precedes, curly equals
⪯ \preceq preceq precedes above single-line equals sign
⪳ \preceqq preceqq precedes above equals sign
⪹ \precnapprox precnapprox precedes above not almost equal to
⪱ \precneq precneq precedes above single-line not equal to
⪵ \precneqq precneqq precedes above not equal to
⋨ \precnsim precnsim precedes, not similar
≾ \precsim precsim precedes, similar
′ \prime prime prime or minute, not superscripted
∏ \prod prod product operator
⌒ \profline profline profile of a line
⌓ \profsurf profsurf profile of a surface
⅊ \PropertyLine PropertyLine property line
∝ \propto propto is proportional to
⊰ \prurel prurel element precedes under relation
⟓ \pullback pullback lower right corner with dot
⟔ \pushout pushout upper left corner with dot
∎ \QED QED end of proof
⁗ \qprime qprime quadruple prime, not superscripted
♩ \quarternote quarternote music note (sung text sign)
≟ \questeq questeq equal with questionmark
⁇ \Question Question double question mark
⟩ \rangle rangle mathematical right angle bracket
⟫ \rAngle rAngle mathematical right double angle bracket
⦒ \rangledot rangledot right angle bracket with dot
⍼ \rangledownzigzagarrow rangledownzigzagarrow right angle with downwards zigzag arrow
⟆ \rbag rbag right s-shaped bag delimiter
⦘ \rblkbrbrak rblkbrbrak right black tortoise shell bracket
} \rbrace rbrace right curly bracket
⦄ \rBrace rBrace right white curly bracket
⎭ \rbracelend rbracelend right curly bracket lower hook
⎬ \rbracemid rbracemid right curly bracket middle piece
⎫ \rbraceuend rbraceuend right curly bracket upper hook
] \rbrack rbrack right square bracket
⟧ \rBrack rBrack mathematical right white square bracket
⎥ \rbrackextender rbrackextender right square bracket extension
⎦ \rbracklend rbracklend right square bracket lower corner
⦎ \rbracklrtick rbracklrtick right square bracket with tick in bottom corner
⦌ \rbrackubar rbrackubar right square bracket with underbar
⎤ \rbrackuend rbrackuend right square bracket upper corner
⦐ \rbrackurtick rbrackurtick right square bracket with tick in top corner
❳ \rbrbrak rbrbrak light right tortoise shell bracket ornament
⟭ \Rbrbrak Rbrbrak mathematical right white tortoise shell bracket
⌉ \rceil rceil right ceiling
⧽ \rcurvyangle rcurvyangle right pointing curved angle bracket
⤫ \rdiagovfdiag rdiagovfdiag rising diagonal crossing falling diagonal
⤰ \rdiagovsearrow rdiagovsearrow rising diagonal crossing south east arrow
↳ \Rdsh Rdsh right down angled arrow
ℜ \Re Re real part
⦣ \revangle revangle reversed angle
⦥ \revangleubar revangleubar reversed angle with underbar
⦰ \revemptyset revemptyset reversed empty set
⧵ \reversesolidus reversesolidus reverse solidus
⫮ \revnmid revnmid does not divide with reversed negation slash
⧒ \rfbowtie rfbowtie right black bowtie
⌋ \rfloor rfloor right floor
⧕ \rftimes rftimes right black times
⟯ \rgroup rgroup mathematical right flattened parenthesis
∟ \rightangle rightangle right (90 degree) angle
⦝ \rightanglemdot rightanglemdot measured right angle with dot
⦜ \rightanglesqr rightanglesqr right angle variant with square
→ \rightarrow rightarrow /rightarrow /to a: rightward arrow
⇒ \Rightarrow Rightarrow implies
⥵ \rightarrowapprox rightarrowapprox rightwards arrow above almost equal to
⭈ \rightarrowbackapprox rightarrowbackapprox rightwards arrow above reverse almost equal to
⇥ \rightarrowbar rightarrowbar rightwards arrow to bar
⭌ \rightarrowbsimilar rightarrowbsimilar righttwards arrow above reverse tilde operator
⤞ \rightarrowdiamond rightarrowdiamond rightwards arrow to black diamond
⭃ \rightarrowgtr rightarrowgtr rightwards arrow through greater-than
⟴ \rightarrowonoplus rightarrowonoplus right arrow with circled plus
⥅ \rightarrowplus rightarrowplus rightwards arrow with plus below
⥂ \rightarrowshortleftarrow rightarrowshortleftarrow rightwards arrow above short leftwards arrow
⥴ \rightarrowsimilar rightarrowsimilar rightwards arrow above tilde operator
⭄ \rightarrowsupset rightarrowsupset rightwards arrow through subset
↣ \rightarrowtail rightarrowtail right arrow-tailed
⇾ \rightarrowtriangle rightarrowtriangle rightwards open-headed arrow
⥇ \rightarrowx rightarrowx rightwards arrow through x
⤍ \rightbkarrow rightbkarrow rightwards double dash arrow
⤳ \rightcurvedarrow rightcurvedarrow wave arrow pointing directly right
⇢ \rightdasharrow rightdasharrow rightwards dashed arrow
⤜ \rightdbltail rightdbltail rightwards double arrow-tail
⤑ \rightdotarrow rightdotarrow rightwards arrow with dotted stem
⤷ \rightdowncurvedarrow rightdowncurvedarrow arrow pointing downwards then curving rightwards
⥽ \rightfishtail rightfishtail right fish tail
⃑ \rightharpoonaccent rightharpoonaccent combining right harpoon above
⇁ \rightharpoondown rightharpoondown right harpoon-down
⥗ \rightharpoondownbar rightharpoondownbar rightwards harpoon with barb down to bar
⥤ \rightharpoonsupdown rightharpoonsupdown rightwards harpoon with barb up above rightwards harpoon with barb down
⇀ \rightharpoonup rightharpoonup right harpoon-up
⥓ \rightharpoonupbar rightharpoonupbar rightwards harpoon with barb up to bar
⥬ \rightharpoonupdash rightharpoonupdash rightwards harpoon with barb up above long dash
⥰ \rightimply rightimply right double arrow with rounded head
⇄ \rightleftarrows rightleftarrows right arrow over left arrow
⇌ \rightleftharpoons rightleftharpoons right harpoon over left
⥩ \rightleftharpoonsdown rightleftharpoonsdown rightwards harpoon with barb down above leftwards harpoon with barb down
⥨ \rightleftharpoonsup rightleftharpoonsup rightwards harpoon with barb up above leftwards harpoon with barb up
☽ \rightmoon rightmoon first quarter moon
⟖ \rightouterjoin rightouterjoin right outer join
⭔ \rightpentagon rightpentagon white right-pointing pentagon
⭓ \rightpentagonblack rightpentagonblack black right-pointing pentagon
⇉ \rightrightarrows rightrightarrows two right arrows
⇝ \rightsquigarrow rightsquigarrow rightwards squiggle arrow
⤚ \righttail righttail rightwards arrow-tail
⇶ \rightthreearrows rightthreearrows three rightwards arrows
⋌ \rightthreetimes rightthreetimes right semidirect product
↝ \rightwavearrow rightwavearrow right arrow-wavy
⇨ \rightwhitearrow rightwhitearrow rightwards white arrow
⨢ \ringplus ringplus plus sign with small circle above
≓ \risingdotseq risingdotseq equals, rising dots
⎱ \rmoustache rmoustache upper right or lower left curly bracket section
) \rparen rparen right parenthesis
⦆ \rParen rParen right white parenthesis
⎟ \rparenextender rparenextender right parenthesis extension
⦔ \rparengtr rparengtr right arc greater-than bracket
⎠ \rparenlend rparenlend right parenthesis lower hook
⦖ \Rparenless Rparenless double right arc less-than bracket
⎞ \rparenuend rparenuend right parenthesis upper hook
⨒ \rppolint rppolint line integration with rectangular path around pole
⦊ \rrangle rrangle z notation right binding bracket
⇛ \Rrightarrow Rrightarrow right triple arrow
⭆ \RRightarrow RRightarrow rightwards quadruple arrow
⦈ \rrparenthesis rrparenthesis z notation right image bracket
↱ \Rsh Rsh /rsh a:
⧷ \rsolbar rsolbar reverse solidus with horizontal stroke
⫎ \rsqhook rsqhook square right open box operator
⩥ \rsub rsub z notation range antirestriction
⋊ \rtimes rtimes times sign, right closed
⧎ \rtriltri rtriltri right triangle above left triangle
⧴ \ruledelayed ruledelayed rule-delayed
⎹ \rvboxline rvboxline right vertical box line
⧙ \rvzigzag rvzigzag right wiggly fence
⧛ \Rvzigzag Rvzigzag right double wiggly fence
⅃ \sansLmirrored sansLmirrored reversed sans-serif capital l
⅂ \sansLturned sansLturned turned sans-serif capital l
⨓ \scpolint scpolint line integration with semicircular path around pole
⊱ \scurel scurel succeeds under relation
↘ \searrow searrow se pointing arrow
⇘ \Searrow Searrow se pointing double arrow
⤭ \seovnearrow seovnearrow south east arrow crossing north east arrow
∖ \setminus setminus set minus (cf. reverse solidus)
♯ \sharp sharp musical sharp
⫟ \shortdowntack shortdowntack short down tack
⫞ \shortlefttack shortlefttack short left tack
⥄ \shortrightarrowleftarrow shortrightarrowleftarrow short rightwards arrow above leftwards arrow
⫠ \shortuptack shortuptack short up tack
⧢ \shuffle shuffle shuffle product
∼ \sim sim similar
≃ \sime sime similar, equals (alias)
≃ \simeq simeq similar, equals
⪠ \simgE simgE similar above greater-than above equals sign
⪞ \simgtr simgtr similar or greater-than
⭉ \similarleftarrow similarleftarrow tilde operator above leftwards arrow
⥲ \similarrightarrow similarrightarrow tilde operator above rightwards arrow
⪟ \simlE simlE similar above less-than above equals sign
⪝ \simless simless similar or less-than
⩬ \simminussim simminussim similar minus similar
≆ \simneqq simneqq similar, not equals [vert only for 9573 entity]
⨤ \simplus simplus plus sign with tilde above
⩫ \simrdots simrdots tilde operator with rising dots
∿ \sinewave sinewave sine wave
◂ \smallblacktriangleleft smallblacktriangleleft left triangle, filled
▸ \smallblacktriangleright smallblacktriangleright right triangle, filled
∊ \smallin smallin set membership (small set membership)
∍ \smallni smallni /ni /owns r: contains (small contains as member)
◃ \smalltriangleleft smalltriangleleft left triangle, open
▹ \smalltriangleright smalltriangleright right triangle, open
⨳ \smashtimes smashtimes smash product
• \smblkcircle smblkcircle /bullet b: round bullet, filled
⬩ \smblkdiamond smblkdiamond black small diamond
⬪ \smblklozenge smblklozenge black small lozenge
▪ \smblksquare smblksquare /blacksquare - sq bullet, filled
⧤ \smeparsl smeparsl equals sign and slanted parallel with tilde above
⌣ \smile smile up curve
⪪ \smt smt smaller than
⪬ \smte smte smaller than or equal to
⭒ \smwhitestar smwhitestar white small star
◦ \smwhtcircle smwhtcircle white bullet
⋄ \smwhtdiamond smwhtdiamond white diamond
⬫ \smwhtlozenge smwhtlozenge white small lozenge
▫ \smwhtsquare smwhtsquare white small square
♠ \spadesuit spadesuit spades suit symbol
∢ \sphericalangle sphericalangle angle-spherical
⦡ \sphericalangleup sphericalangleup spherical angle opening up
⊓ \sqcap sqcap square product (sqcap)
⩎ \Sqcap Sqcap double square intersection
⊔ \sqcup sqcup square union
⩏ \Sqcup Sqcup double square union
⨖ \sqint sqint quaternion integral operator
⌑ \sqlozenge sqlozenge square lozenge
√ \sqrt sqrt radical
⎷ \sqrtbottom sqrtbottom radical symbol bottom
⊏ \sqsubset sqsubset square subset
⊑ \sqsubseteq sqsubseteq square subset, equals
⋤ \sqsubsetneq sqsubsetneq square subset, not equals
⊐ \sqsupset sqsupset square superset
⊒ \sqsupseteq sqsupseteq square superset, equals
⋥ \sqsupsetneq sqsupsetneq square superset, not equals
⬓ \squarebotblack squarebotblack square with bottom half black
▩ \squarecrossfill squarecrossfill square with diagonal crosshatch fill
▤ \squarehfill squarehfill square, horizontal rule filled
▦ \squarehvfill squarehvfill square with orthogonal crosshatch fill
◧ \squareleftblack squareleftblack square, filled left half
⬕ \squarellblack squarellblack square with lower left diagonal half black
◱ \squarellquad squarellquad white square with lower left quadrant
◪ \squarelrblack squarelrblack square, filled bottom right corner
◲ \squarelrquad squarelrquad white square with lower right quadrant
▨ \squareneswfill squareneswfill square, ne-to-sw rule filled
▧ \squarenwsefill squarenwsefill square, nw-to-se rule filled
◨ \squarerightblack squarerightblack square, filled right half
⬒ \squaretopblack squaretopblack square with top half black
◩ \squareulblack squareulblack square, filled top left corner
◰ \squareulquad squareulquad white square with upper left quadrant
⬔ \squareurblack squareurblack square with upper right diagonal half black
◳ \squareurquad squareurquad white square with upper right quadrant
▥ \squarevfill squarevfill square, vertical rule filled
▢ \squoval squoval white square with rounded corners
⫽ \sslash sslash double solidus operator
⋆ \star star small star, filled, low
≛ \stareq stareq star equals
⏤ \strns strns straightness
⫃ \subedot subedot subset of or equal to with dot above
⫁ \submult submult subset with multiplication sign below
⥹ \subrarr subrarr subset above rightwards arrow
⊂ \subset subset subset or is implied by
⋐ \Subset Subset double subset
⫉ \subsetapprox subsetapprox subset of above almost equal to
⟃ \subsetcirc subsetcirc open subset
⪽ \subsetdot subsetdot subset with dot
⊆ \subseteq subseteq subset, equals
⫅ \subseteqq subseteqq subset of above equals sign
⊊ \subsetneq subsetneq subset, not equals
⫋ \subsetneqq subsetneqq subset of above not equal to
⪿ \subsetplus subsetplus subset with plus sign below
⫇ \subsim subsim subset of above tilde operator
⫕ \subsub subsub subset above subset
⫓ \subsup subsup subset above superset
≻ \succ succ succeeds
⪼ \Succ Succ double succeeds
⪸ \succapprox succapprox succeeds above almost equal to
≽ \succcurlyeq succcurlyeq succeeds, curly equals
⪰ \succeq succeq succeeds above single-line equals sign
⪴ \succeqq succeqq succeeds above equals sign
⪺ \succnapprox succnapprox succeeds above not almost equal to
⪲ \succneq succneq succeeds above single-line not equal to
⪶ \succneqq succneqq succeeds above not equal to
⋩ \succnsim succnsim succeeds, not similar
≿ \succsim succsim succeeds, similar
∑ \sum sum summation operator
⎳ \sumbottom sumbottom summation bottom
⨋ \sumint sumint summation with integral
⎲ \sumtop sumtop summation top
☼ \sun sun white sun with rays
⫘ \supdsub supdsub superset beside and joined by dash with subset
⫄ \supedot supedot superset of or equal to with dot above
⟉ \suphsol suphsol superset preceding solidus
⫗ \suphsub suphsub superset beside subset
⥻ \suplarr suplarr superset above leftwards arrow
⫂ \supmult supmult superset with multiplication sign below
⊃ \supset supset superset or implies
⋑ \Supset Supset double superset
⫊ \supsetapprox supsetapprox superset of above almost equal to
⟄ \supsetcirc supsetcirc open superset
⪾ \supsetdot supsetdot superset with dot
⊇ \supseteq supseteq superset, equals
⫆ \supseteqq supseteqq superset of above equals sign
⊋ \supsetneq supsetneq superset, not equals
⫌ \supsetneqq supsetneqq superset of above not equal to
⫀ \supsetplus supsetplus superset with plus sign below
⫈ \supsim supsim superset of above tilde operator
⫔ \supsub supsub superset above subset
⫖ \supsup supsup superset above superset
√ \surd surd radical
↙ \swarrow swarrow sw pointing arrow
⇙ \Swarrow Swarrow sw pointing double arrow
⫾ \talloblong talloblong white vertical bar
∴ \therefore therefore therefore
⧧ \thermod thermod thermodynamic
⟀ \threedangle threedangle three dimensional angle
⫶ \threedotcolon threedotcolon triple colon operator
⃨ \threeunderdot threeunderdot combining triple underdot
⁀ \tieconcat tieconcat character tie, z notation sequence concatenation
⧝ \tieinfty tieinfty tie over infinity
̃ \tilde tilde tilde
× \times times multiply sign
⨱ \timesbar timesbar multiplication sign with underbar
⧿ \tminus tminus miny
⤨ \toea toea north east arrow and south east arrow
⤧ \tona tona north west arrow and north east arrow
⊤ \top top top
⌶ \topbot topbot top and bottom
⫱ \topcir topcir down tack with circle below
⫚ \topfork topfork pitchfork with tee top
◠ \topsemicircle topsemicircle upper half circle
⤩ \tosa tosa south east arrow and south west arrow
⤪ \towa towa south west arrow and north west arrow
⧾ \tplus tplus tiny
⏢ \trapezium trapezium white trapezium
◬ \trianglecdot trianglecdot triangle with centered dot
▿ \triangledown triangledown down triangle, open
◁ \triangleleft triangleleft (large) left triangle, open; z notation domain restriction
◭ \triangleleftblack triangleleftblack up-pointing triangle with left half black
⊴ \trianglelefteq trianglelefteq left triangle, equals
⨺ \triangleminus triangleminus minus sign in triangle
⧊ \triangleodot triangleodot triangle with dot above
⨹ \triangleplus triangleplus plus sign in triangle
≜ \triangleq triangleq triangle, equals
▷ \triangleright triangleright (large) right triangle, open; z notation range restriction
◮ \trianglerightblack trianglerightblack up-pointing triangle with right half black
⊵ \trianglerighteq trianglerighteq right triangle, equals
⧌ \triangles triangles s in triangle
⧍ \triangleserifs triangleserifs triangle with serifs at bottom
⨻ \triangletimes triangletimes multiplication sign in triangle
⧋ \triangleubar triangleubar triangle with underbar
⧻ \tripleplus tripleplus triple plus
‴ \trprime trprime triple prime (not superscripted)
⫻ \trslash trslash triple solidus binary relation
⦢ \turnangle turnangle turned angle
℩ \turnediota turnediota turned iota
⌙ \turnednot turnednot turned not sign
⩋ \twocaps twocaps intersection beside and joined with intersection
⩊ \twocups twocups union beside and joined with union
↡ \twoheaddownarrow twoheaddownarrow down two-headed arrow
↞ \twoheadleftarrow twoheadleftarrow left two-headed arrow
⬻ \twoheadleftarrowtail twoheadleftarrowtail leftwards two-headed arrow with tail
⬷ \twoheadleftdbkarrow twoheadleftdbkarrow leftwards two-headed triple-dash arrow
⬶ \twoheadmapsfrom twoheadmapsfrom leftwards two-headed arrow from bar
⤅ \twoheadmapsto twoheadmapsto rightwards two-headed arrow from bar
↠ \twoheadrightarrow twoheadrightarrow right two-headed arrow
⤖ \twoheadrightarrowtail twoheadrightarrowtail rightwards two-headed arrow with tail
↟ \twoheaduparrow twoheaduparrow up two-headed arrow
⥉ \twoheaduparrowcircle twoheaduparrowcircle upwards two-headed arrow from small circle
‗ \twolowline twolowline double low line (spacing)
♫ \twonotes twonotes beamed eighth notes
⦂ \typecolon typecolon z notation type colon
⏡ \ubrbrak ubrbrak bottom tortoise shell bracket (mathematical use)
◜ \ularc ularc upper left quadrant circular arc
◤ \ulblacktriangle ulblacktriangle upper left triangle, filled
⌜ \ulcorner ulcorner upper left corner
◸ \ultriangle ultriangle upper left triangle
⩁ \uminus uminus union with minus sign
⏟ \underbrace underbrace bottom curly bracket (mathematical use)
⎵ \underbracket underbracket bottom square bracket
⃮ \underleftarrow underleftarrow combining left arrow below
⃭ \underleftharpoondown underleftharpoondown combining leftwards harpoon with barb downwards
͍ \underleftrightarrow underleftrightarrow underleftrightarrow accent
⏝ \underparen underparen bottom parenthesis (mathematical use)
⃯ \underrightarrow underrightarrow combining right arrow below
⃬ \underrightharpoondown underrightharpoondown combining rightwards harpoon with barb downwards
⋯ \unicodecdots unicodecdots three dots, centered
… \unicodeellipsis unicodeellipsis ellipsis (horizontal)
⅋ \upand upand turned ampersand
↑ \uparrow uparrow upward arrow
⇑ \Uparrow Uparrow up double arrow
⤉ \uparrowbarred uparrowbarred upwards arrow with horizontal stroke
⦽ \uparrowoncircle uparrowoncircle up arrow through circle
϶ \upbackepsilon upbackepsilon greek reversed lunate epsilon symbol
⇡ \updasharrow updasharrow upwards dashed arrow
ϝ \updigamma updigamma old greek small letter digamma
Ϝ \upDigamma upDigamma capital digamma
↕ \updownarrow updownarrow up and down arrow
⇕ \Updownarrow Updownarrow up and down double arrow
↨ \updownarrowbar updownarrowbar up down arrow with base (perpendicular)
⇅ \updownarrows updownarrows up arrow, down arrow
⥑ \updownharpoonleftleft updownharpoonleftleft up barb left down barb left harpoon
⥍ \updownharpoonleftright updownharpoonleftright up barb left down barb right harpoon
⥌ \updownharpoonrightleft updownharpoonrightleft up barb right down barb left harpoon
⥏ \updownharpoonrightright updownharpoonrightright up barb right down barb right harpoon
⥮ \updownharpoonsleftright updownharpoonsleftright upwards harpoon with barb left beside downwards harpoon with barb right
⥾ \upfishtail upfishtail up fish tail
↿ \upharpoonleft upharpoonleft up harpoon-left
⥠ \upharpoonleftbar upharpoonleftbar upwards harpoon with barb left from bar
↾ \upharpoonright upharpoonright /upharpoonright /restriction a: up harpoon-right
⥜ \upharpoonrightbar upharpoonrightbar upwards harpoon with barb right from bar
⥣ \upharpoonsleftright upharpoonsleftright upwards harpoon with barb left beside upwards harpoon with barb right
⟒ \upin upin element of opening upwards
⨛ \upint upint integral with overbar
⊎ \uplus uplus plus sign in union
⤴ \uprightcurvearrow uprightcurvearrow arrow pointing rightwards then curving upwards
⇈ \upuparrows upuparrows two up arrows
⇧ \upwhitearrow upwhitearrow upwards white arrow
◝ \urarc urarc upper right quadrant circular arc
◥ \urblacktriangle urblacktriangle upper right triangle, filled
⌝ \urcorner urcorner upper right corner
◹ \urtriangle urtriangle upper right triangle
⤊ \Uuparrow Uuparrow upwards triple arrow
⟰ \UUparrow UUparrow upwards quadruple arrow
⌅ \varbarwedge varbarwedge /barwedge b: logical and, bar above [projective (bar over small wedge)]
⏎ \varcarriagereturn varcarriagereturn return symbol
♧ \varclubsuit varclubsuit club, white (card suit)
♦ \vardiamondsuit vardiamondsuit filled diamond (card suit)
⌆ \vardoublebarwedge vardoublebarwedge /doublebarwedge b: logical and, double bar above [perspective (double bar over small wedge)]
♥ \varheartsuit varheartsuit filled heart (card suit)
⬡ \varhexagon varhexagon white hexagon
⬢ \varhexagonblack varhexagonblack black hexagon
⌬ \varhexagonlrbonds varhexagonlrbonds six carbon ring, corner down, double bonds lower right etc
⋶ \varisinobar varisinobar element of with overbar
⋳ \varisins varisins element of with vertical bar at end of horizontal stroke
⊿ \varlrtriangle varlrtriangle right triangle
⋽ \varniobar varniobar contains with overbar
⋻ \varnis varnis contains with vertical bar at end of horizontal stroke
∅ \varnothing varnothing circle, slash
∲ \varointclockwise varointclockwise contour integral, clockwise
♤ \varspadesuit varspadesuit spade, white (card suit)
✶ \varstar varstar six pointed black star
▵ \vartriangle vartriangle /triangle - up triangle, open
⊲ \vartriangleleft vartriangleleft left triangle, open, variant
⊳ \vartriangleright vartriangleright right triangle, open, variant
⫦ \varVdash varVdash long dash from left member of double vertical
⩡ \varveebar varveebar small vee with underbar
⫨ \vBar vBar short up tack with underbar
⫫ \Vbar Vbar double up tack
⫩ \vBarv vBarv short up tack above short down tack
⎪ \vbraceextender vbraceextender curly bracket extension
⧐ \vbrtri vbrtri vertical bar beside right triangle
⊢ \vdash vdash vertical, dash
⊨ \vDash vDash vertical, double dash
⊩ \Vdash Vdash double vertical, dash
⊫ \VDash VDash double vert, double dash
⫢ \vDdash vDdash vertical bar triple right turnstile
⋮ \vdots vdots vertical ellipsis
⃗ \vec vec combining right arrow above
⨯ \vectimes vectimes vector or cross product
∨ \vee vee /vee /lor b: logical or
⩔ \Vee Vee double logical or
⊻ \veebar veebar logical or, bar below (large vee); exclusive disjunction
⟇ \veedot veedot or with dot inside
⩣ \veedoublebar veedoublebar logical or with double underbar
≚ \veeeq veeeq logical or, equals
⩛ \veemidvert veemidvert logical or with middle stem
⩒ \veeodot veeodot logical or with dot above
⩖ \veeonvee veeonvee two intersecting logical or
⩙ \veeonwedge veeonwedge logical or overlapping logical and
| \vert vert vertical bar
‖ \Vert Vert double vertical bar
⃒ \vertoverlay vertoverlay combining long vertical line overlay
⌗ \viewdata viewdata viewdata square
⟝ \vlongdash vlongdash long left tack
▯ \vrectangle vrectangle rectangle, white (vertical)
▮ \vrectangleblack vrectangleblack black vertical rectangle
⊪ \Vvdash Vvdash triple vertical, dash
⦀ \Vvert Vvert triple vertical bar delimiter
∙ \vysmblkcircle vysmblkcircle bullet operator
⬝ \vysmblksquare vysmblksquare black very small square
∘ \vysmwhtcircle vysmwhtcircle composite function (small circle)
⬞ \vysmwhtsquare vysmwhtsquare white very small square
⦚ \vzigzag vzigzag vertical zigzag line
∧ \wedge wedge /wedge /land b: logical and
⩓ \Wedge Wedge double logical and
⩟ \wedgebar wedgebar logical and with underbar
⟑ \wedgedot wedgedot and with dot
⩠ \wedgedoublebar wedgedoublebar logical and with double underbar
⩚ \wedgemidvert wedgemidvert logical and with middle stem
⩑ \wedgeodot wedgeodot logical and with dot above
⩕ \wedgeonwedge wedgeonwedge two intersecting logical and
≙ \wedgeq wedgeq corresponds to (wedge, equals)
⇪ \whitearrowupfrombar whitearrowupfrombar upwards white arrow from bar
⟁ \whiteinwhitetriangle whiteinwhitetriangle white triangle containing small white triangle
◅ \whitepointerleft whitepointerleft white left-pointing pointer
▻ \whitepointerright whitepointerright white right-pointing pointer
⟤ \whitesquaretickleft whitesquaretickleft white square with leftwards tick
⟥ \whitesquaretickright whitesquaretickright white square with rightwards tick
⬭ \whthorzoval whthorzoval white horizontal ellipse
⬯ \whtvertoval whtvertoval white vertical ellipse
⦦ \wideangledown wideangledown oblique angle opening up
⦧ \wideangleup wideangleup oblique angle opening down
̆ \widebreve widebreve stretchy breve
⃩ \widebridgeabove widebridgeabove combining wide bridge above
̌ \widecheck widecheck stretchy caron
̂ \widehat widehat circumflex accent
̅ \wideoverbar wideoverbar stretchy overbar embellishment
̃ \widetilde widetilde tilde
̰ \wideutilde wideutilde under tilde accent (multiple characters and non-spacing)
℘ \wp wp weierstrass p
≀ \wr wr wreath product
⧹ \xbsol xbsol big reverse solidus
⧸ \xsol xsol big solidus
⅄ \Yup Yup turned sans-serif capital y
Ƶ \Zbar Zbar impedance (latin capital letter z with stroke)
⨟ \zcmp zcmp z notation schema composition
⨠ \zpipe zpipe z notation schema piping
⨡ \zproject zproject z notation schema projection
² \^two superscript-two superscript two
³ \^three superscript-three superscript three
¹ \^one superscript-one superscript one
ٖ \_alef subscript-alef arabic subscript alef
ٰ \^alef superscript-alef arabic letter superscript alef
ܑ \^alaph superscript-alaph syriac letter superscript alaph
࢝ \^alefmokhassas superscript-alef-mokhassas arabic superscript alef mokhassas
ᵢ \_smallletteri subscript-small-letter-i latin subscript small letter i
ᵣ \_smallletterr subscript-small-letter-r latin subscript small letter r
ᵤ \_smallletteru subscript-small-letter-u latin subscript small letter u
ᵥ \_smallletterv subscript-small-letter-v latin subscript small letter v
ᵦ \_smallletterbeta subscript-small-letter-beta greek subscript small letter beta
ᵧ \_smalllettergamma subscript-small-letter-gamma greek subscript small letter gamma
ᵨ \_smallletterrho subscript-small-letter-rho greek subscript small letter rho
ᵩ \_smallletterphi subscript-small-letter-phi greek subscript small letter phi
ᵪ \_smallletterchi subscript-small-letter-chi greek subscript small letter chi
⁰ \^zero superscript-zero superscript zero
ⁱ \^latinsmallletteri superscript-latin-small-letter-i superscript latin small letter i
⁴ \^four superscript-four superscript four
⁵ \^five superscript-five superscript five
⁶ \^six superscript-six superscript six
⁷ \^seven superscript-seven superscript seven
⁸ \^eight superscript-eight superscript eight
⁹ \^nine superscript-nine superscript nine
⁺ \^plussign superscript-plus-sign superscript plus sign
⁻ \^minus superscript-minus superscript minus
⁼ \^equalssign superscript-equals-sign superscript equals sign
⁽ \^leftparenthesis superscript-left-parenthesis superscript left parenthesis
⁾ \^rightparenthesis superscript-right-parenthesis superscript right parenthesis
ⁿ \^latinsmalllettern superscript-latin-small-letter-n superscript latin small letter n
₀ \_zero subscript-zero subscript zero
₁ \_one subscript-one subscript one
₂ \_two subscript-two subscript two
₃ \_three subscript-three subscript three
₄ \_four subscript-four subscript four
₅ \_five subscript-five subscript five
₆ \_six subscript-six subscript six
₇ \_seven subscript-seven subscript seven
₈ \_eight subscript-eight subscript eight
₉ \_nine subscript-nine subscript nine
₊ \_plussign subscript-plus-sign subscript plus sign
₋ \_minus subscript-minus subscript minus
₌ \_equalssign subscript-equals-sign subscript equals sign
₍ \_leftparenthesis subscript-left-parenthesis subscript left parenthesis
₎ \_rightparenthesis subscript-right-parenthesis subscript right parenthesis
ₐ \_smalllettera subscript-small-letter-a latin subscript small letter a
ₑ \_smalllettere subscript-small-letter-e latin subscript small letter e
ₒ \_smalllettero subscript-small-letter-o latin subscript small letter o
ₓ \_smallletterx subscript-small-letter-x latin subscript small letter x
ₔ \_smallletterschwa subscript-small-letter-schwa latin subscript small letter schwa
ₕ \_smallletterh subscript-small-letter-h latin subscript small letter h
ₖ \_smallletterk subscript-small-letter-k latin subscript small letter k
ₗ \_smallletterl subscript-small-letter-l latin subscript small letter l
ₘ \_smallletterm subscript-small-letter-m latin subscript small letter m
ₙ \_smalllettern subscript-small-letter-n latin subscript small letter n
ₚ \_smallletterp subscript-small-letter-p latin subscript small letter p
ₛ \_smallletters subscript-small-letter-s latin subscript small letter s
ₜ \_smalllettert subscript-small-letter-t latin subscript small letter t
⨧ \_two subscript-two plus sign with subscript two
ⱼ \_smallletterj subscript-small-letter-j latin subscript small letter j
ﱛ \^alefisolatedform superscript-alef-isolated-form arabic ligature thal with superscript alef isolated form
ﱜ \^alefisolatedform superscript-alef-isolated-form arabic ligature reh with superscript alef isolated form
ﱝ \^alefisolatedform superscript-alef-isolated-form arabic ligature alef maksura with superscript alef isolated form
ﱣ \^alefisolatedform superscript-alef-isolated-form arabic ligature shadda with superscript alef isolated form
ﲐ \^aleffinalform superscript-alef-final-form arabic ligature alef maksura with superscript alef final form
ﳙ \^alefinitialform superscript-alef-initial-form arabic ligature heh with superscript alef initial form
𐞁 \^triangularcolon superscript-triangular-colon modifier letter superscript triangular colon
𐞂 \^halftriangularcolon superscript-half-triangular-colon modifier letter superscript half triangular colon
𞁑 \_smalllettera subscript-small-letter-a cyrillic subscript small letter a
𞁒 \_smallletterbe subscript-small-letter-be cyrillic subscript small letter be
𞁓 \_smallletterve subscript-small-letter-ve cyrillic subscript small letter ve
𞁔 \_smallletterghe subscript-small-letter-ghe cyrillic subscript small letter ghe
𞁕 \_smallletterde subscript-small-letter-de cyrillic subscript small letter de
𞁖 \_smallletterie subscript-small-letter-ie cyrillic subscript small letter ie
𞁗 \_smallletterzhe subscript-small-letter-zhe cyrillic subscript small letter zhe
𞁘 \_smallletterze subscript-small-letter-ze cyrillic subscript small letter ze
𞁙 \_smallletteri subscript-small-letter-i cyrillic subscript small letter i
𞁚 \_smallletterka subscript-small-letter-ka cyrillic subscript small letter ka
𞁛 \_smallletterel subscript-small-letter-el cyrillic subscript small letter el
𞁜 \_smalllettero subscript-small-letter-o cyrillic subscript small letter o
𞁝 \_smallletterpe subscript-small-letter-pe cyrillic subscript small letter pe
𞁞 \_smallletteres subscript-small-letter-es cyrillic subscript small letter es
𞁟 \_smallletteru subscript-small-letter-u cyrillic subscript small letter u
𞁠 \_smallletteref subscript-small-letter-ef cyrillic subscript small letter ef
𞁡 \_smallletterha subscript-small-letter-ha cyrillic subscript small letter ha
𞁢 \_smalllettertse subscript-small-letter-tse cyrillic subscript small letter tse
𞁣 \_smallletterche subscript-small-letter-che cyrillic subscript small letter che
𞁤 \_smalllettersha subscript-small-letter-sha cyrillic subscript small letter sha
𞁥 \_smallletterhardsign subscript-small-letter-hard-sign cyrillic subscript small letter hard sign
𞁦 \_smallletteryeru subscript-small-letter-yeru cyrillic subscript small letter yeru
𞁧 \_smallletterghewithupturn subscript-small-letter-ghe-with-upturn cyrillic subscript small letter ghe with upturn
𞁨 \_smallletterbyelorussianukrainiani subscript-small-letter-byelorussian-ukrainian-i cyrillic subscript small letter byelorussian-ukrainian i
𞁩 \_smallletterdze subscript-small-letter-dze cyrillic subscript small letter dze
𞁪 \_smallletterdzhe subscript-small-letter-dzhe cyrillic subscript small letter dzhe
