# Bitcoin blockchain trivia: a short guide

Bitcoin's blockchain records payments, but people have also used its
transaction and block fields for messages, memorials, images, audio, code,
political statements, jokes, and experiments. The entries below briefly
describe `52` verified examples and link to a public chain record for each.

A chain record proves that particular bytes were confirmed; it does not by
itself prove authorship, intent, or the truth of an embedded claim. Labels
such as Ordinals and AtomSea belong to application-layer interpretations,
not to Bitcoin's base consensus rules.

## Genesis began with a bailout headline

**Chain context:** 3 JAN 2009 · BLOCK 0 · COINBASE INPUT · [Inspect the chain record](https://mempool.space/block/000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f)

Satoshi placed a Times headline about a second bank bailout in Bitcoin's first block. It works as a lower-bound timestamp and as a pointed monetary-policy reference. The genesis reward is itself unusual: it is not spendable through normal chain history.

*Why it stands out:* Bitcoin's opening block reads like a tiny editorial about the financial system it entered.

## Bitcoin's first recipient was Hal Finney

**Chain context:** 12 JAN 2009 · BLOCK 170 · 10 BTC · [Inspect the chain record](https://mempool.space/tx/f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16)

Satoshi sent 10 BTC to Hal Finney and returned the rest of a 50 BTC coinbase output as change. The transaction carries no prose; its content is historical—the first widely recognized transfer between two people on the live network.

*Why it stands out:* Bitcoin's first human recipient had already spent decades building privacy and digital-cash infrastructure.

## Two pizzas became a 10,000 BTC receipt

**Chain context:** 22 MAY 2010 · 10,000 BTC · 0.99 BTC FEE · [Inspect the chain record](https://mempool.space/tx/a1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d)

Laszlo Hanyecz traded 10,000 BTC for two delivered pizzas. Jeremy Sturdivant accepted the offer and ordered them. The chain shows the payment—not the food—so the famous story depends on the contemporaneous forum record.

*Why it stands out:* A mundane meal became Bitcoin's recurring benchmark for real-world usability and changing exchange value.

## A JPEG logo hid inside fake addresses

**Chain context:** 13 MAY 2011 · 8,776-BYTE JPEG · TWO TRANSACTIONS · [Inspect the chain record](https://mempool.space/tx/ceb1a7fb57ef8b75ac59b56dd859d5cb3ab5c31168aa55eb3819cd5ddbd3d806)

The Bitcoin logo was yEnc-encoded and spread across output fields that looked like address hashes. Reading the disguised bytes in order reconstructs bitcoin.jpg. This predates the standard OP_RETURN carrier.

*Why it stands out:* The payment network became an accidental image archive before it had a conventional data output.

## A mining-pool prayer war ended in a rickroll

**Chain context:** 25 AUG 2011 · BLOCK 142,573 · ELIGIUS · [Inspect the chain record](https://mempool.space/block/00000000000005b71bc4c0cf24a6f00e04980c627e9409266983bd37acbe14d3)

During a sequence of religious and atheist coinbase messages, an Eligius-mined block carried a taunting reply and a shortened URL. The link resolved to a rickroll. The artifact sits in the coinbase input, not in an ordinary payment output.

*Why it stands out:* For a moment, miners used proof-of-work blocks like an extremely expensive public message board.

## Len Sassaman received an on-chain memorial

**Chain context:** 30 JUL 2011 · BLOCK 138,725 · ASCII PORTRAIT · [Inspect the chain record](https://mempool.space/tx/930a2114cdaa86e1fac46d15c74e81c09eee1d4150ff9d48e76cb0697d8e1d72)

Dan Kaminsky and Travis Goodspeed embedded an ASCII portrait and memorial text for their friend Len Sassaman shortly after his death. Output scripts carry the tribute a few characters at a time.

*Why it stands out:* A cryptographic ledger became a globally replicated memorial stone for a cryptographer.

## The whitepaper was archived inside Bitcoin

**Chain context:** 6 APR 2013 · 198,724 BYTES · ≈0.596 BTC FEE · [Inspect the chain record](https://mempool.space/tx/54e48e5f5c656b26c3bca14a8c95aa583d07ebe84dde3b7dd4a78f4e4186e713)

One large transaction stores a PDF copy of Satoshi's whitepaper across many output scripts. A decoder must remove the script wrappers and concatenate the disguised payload fragments before a PDF reader can open it.

*Why it stands out:* The document describing Bitcoin was archived inside the system it describes.

## Cablegate came with its own downloader

**Chain context:** APR 2013 · ≈2.5 MB · ≈130 CHUNKS · [Inspect the chain record](https://mempool.space/tx/691dd277dc0e90a462a3d652a1171686de49cf19067cd33c7df0392833fb986a)

An unknown publisher split a compressed WikiLeaks Cablegate archive into transaction chunks, then published an index and a separate transaction containing Python retrieval tools. The index frames the upload as a free-speech act.

*Why it stands out:* The archive was self-describing: the data, chunk list, and recovery tool were all placed on-chain.

## Encrypted files made a permanent secret

**Chain context:** APR 2013 · CAST5 OPENPGP · PLAINTEXT UNKNOWN · [Inspect the chain record](https://mempool.space/tx/7379ab5047b143c0b6cfe5d8d79ad240b4b4f8cced55aa26f86d1d3d370c0d4c)

Three large transactions contain OpenPGP payloads encrypted with CAST5. The format is visible, but the plaintext and passphrase are not. Every archival node can preserve the ciphertext without learning what it says.

*Why it stands out:* Bitcoin can preserve a secret perfectly without making it any less secret.

## The chain preserves a broken BASIC program

**Chain context:** 10 APR 2013 · 6,114 BYTES · CREATURE SIMULATOR · [Inspect the chain record](https://mempool.space/tx/3a1c1cc760bffad4041cbfde56fbb5e29ea58fda416e9f4c4615becd65576fe7)

A transaction carries a BASIC program with creatures, food, movement, breeding, and mutation variables. Technical review found syntax and logic errors severe enough that the program appears unusable without repairs.

*Why it stands out:* The chain permanently preserves not just software, but buggy software.

## An immutable “Satoshi email” is probably fake

**Chain context:** 12 AUG 2013 · EMAIL-LIKE PATCH · AUTHOR UNPROVEN · [Inspect the chain record](https://mempool.space/tx/77822fd6663c665104119cb7635352756dfc50da76a92d417ec1a12c518fad69)

The transaction encodes an email-like message attributed to Satoshi and a Bitcoin code patch. Its presence proves only that someone published those bytes. The timing and context make genuine Satoshi authorship implausible.

*Why it stands out:* An immutable ledger preserves a forgery just as faithfully as it preserves a genuine document.

## One string popped an explorer alert

**Chain context:** 12 AUG 2013 · OP_RETURN · XSS DEMONSTRATION · [Inspect the chain record](https://mempool.space/tx/59bd7b2cff5da929581fc9fef31a2fba14508f1477e366befb1eb42a8810a000)

A short HTML/JavaScript snippet was designed to trigger an alert when an explorer rendered transaction text without safe escaping. Bitcoin itself was not compromised; the vulnerable surface was the web viewer interpreting hostile chain data.

*Why it stands out:* Every explorer, wallet, and indexer must treat blockchain text as untrusted input.

## Mandela received an on-chain obituary

**Chain context:** 7 DEC 2013 · JPEG + BIOGRAPHY + QUOTATIONS · [Inspect the chain record](https://mempool.space/tx/8881a937a437ff6ce83be3a89d77ea88ee12315f37f7ef0dd3742c30eef92dba)

A transaction stores a small JPEG portrait, filename, biographical text, and quotations memorializing Nelson Mandela shortly after his death. Reconstructing the image requires reading payload fragments from output data.

*Why it stands out:* Transaction outputs became a tiny obituary and photo album for a world leader.

## Bitcoin was fully rickrolled

**Chain context:** 5 NOV 2013 · OP_RETURN · FULL SONG LYRICS · [Inspect the chain record](https://mempool.space/tx/d29c9c0e8e4d2a9790922af73f0b8d51f0bd4bb19940d9cf910ead8fbe85bc9b)

An early OP_RETURN transaction stored the complete lyrics of the 1987 song used in the rickroll meme. This guide does not reproduce the copyrighted lyrics; the explorer exposes the historical payload.

*Why it stands out:* Even a global financial ledger is not immune to a classic bait-and-switch prank.

## Mt. Gox got a one-line farewell

**Chain context:** 25 FEB 2014 · OP_RETURN · EXCHANGE SHUTDOWN · [Inspect the chain record](https://mempool.space/tx/0540b5dda23ee870330c6b1e18a88c592cf8d847c47f1dc1d5328f46115b12b3)

On the day Mt. Gox shut down, an OP_RETURN output recorded a dated farewell wishing the failed exchange peace. It captures grief and sarcasm, but it does not prove anything about the exchange's internal state.

*Why it stands out:* A market disaster acquired a permanent one-line epitaph in the settlement ledger.

## The internet's cat found Bitcoin

**Chain context:** 28 SEP 2014 · FAKE OUTPUT DATA · AUTHOR UNKNOWN · [Inspect the chain record](https://mempool.space/tx/7b537ad012439c6306dd74e13ba9c20926d68d04fc0c6da2fc81a8eb8f9ea017)

A transaction's output fields reconstruct a cat made from keyboard characters. It has no stated financial function and no reliable attribution. A normal explorer shows scripts and hex; ordered extraction reveals the drawing.

*Why it stands out:* Cats colonized Bitcoin, just as they colonized the rest of the internet.

## Force of Will became an ASCII collectible

**Chain context:** 3 DEC 2014 · 54 OUTPUTS · TRADING-CARD FANDOM · [Inspect the chain record](https://mempool.space/tx/9a74d0ee2e9a925d9afadc413e087fa2effda031935bf19a0d4d48df76e4ce3f)

The output data reconstructs an ASCII rendition of the famous Magic: The Gathering card Force of Will, including rules text and an artist credit. This guide describes the transaction without reproducing the original card art.

*Why it stands out:* Collectible-card culture reached Bitcoin years before “NFT” became a mainstream label.

## Hypnotoad lives in transaction outputs

**Chain context:** 24 JAN 2015 · 36 OUTPUTS · FUTURAMA REFERENCE · [Inspect the chain record](https://mempool.space/tx/69708943906eb32a320a5a450fed450b0f14b4e475a98bc74615962b68a0bc83)

Output data reconstructs Hypnotoad, the mind-controlling amphibian from Futurama, as ASCII art. It used spendable-looking output structures rather than an Ordinals witness envelope.

*Why it stands out:* All glory to an amphibian hidden among transaction scripts.

## The block-size fight became a rap parody

**Chain context:** 7 MAY 2015 · SCRIPT TEXT · GOVERNANCE CULTURE · [Inspect the chain record](https://mempool.space/tx/08893442680a20c4d0548dec2c8c421fa43336528b4e274dbf2652774f9c9f2d)

A transaction rewrote a well-known rap song into an argument for larger Bitcoin blocks. It is a cultural fossil from the increasingly bitter block-size debate. The derivative lyrics are not reproduced here.

*Why it stands out:* A protocol-governance dispute turned into on-chain musical satire.

## One error message appeared ~13,000 times

**Chain context:** 6 MAR 2016 EXAMPLE · OP_RETURN · SCAN-DERIVED COUNT · [Inspect the chain record](https://mempool.space/tx/a87d406fae047258a12923b3c11a797a5765bd8f868df5c7e9b1cead0e92c9c1)

A campaign repeated the same short congestion-style message in many transactions. Ciro Santilli's scan reports roughly 13,000 occurrences. The exact total depends on matching rules and the chain height analyzed.

*Why it stands out:* The ledger received the blockchain equivalent of a repeated HTTP error page.

## The 2020 halving echoed Genesis

**Chain context:** 11 MAY 2020 · BLOCK 629,999 · F2POOL COINBASE · [Inspect the chain record](https://mempool.space/block/0000000000000000000d656be18bb095db1b23bd797266b0ac3ba720b1962b1e)

The final block before the third subsidy halving carried a New York Times headline about a $2.3 trillion Federal Reserve intervention. F2Pool deliberately echoed the crisis-era headline in the Genesis Block.

*Why it stands out:* Eleven years later, a miner answered Bitcoin's opening sentence with another monetary-crisis headline.

## Block 666,666 turned into a Bible puzzle

**Chain context:** 18 JAN 2021 · BLOCK 666,666 · OP_RETURN + VANITY ADDRESSES · [Inspect the chain record](https://mempool.space/block/0000000000000000000b7b8574bc6fd285825ec2dbcbeca149121fc05b0c828c)

One transaction quoted Romans 12:21 and paid vanity addresses beginning 1GoD… and 1BibLE…. The choreography is application-level theater: a block height is a sequence number, not a consensus symbol.

*Why it stands out:* Height, scripture, message, and vanity addresses were coordinated into one elaborate chain puzzle.

## Inscription zero is a 100-pixel skull

**Chain context:** 14 DEC 2022 · BLOCK 767,430 · PNG IN TAPROOT WITNESS · [Inspect the chain record](https://mempool.space/tx/6fb976ab49dcec017f1e201e84395983204ae1a7c2abf7ced0a85d692e442799)

Casey Rodarmor's first Ordinals inscription is a 100 × 100 black-and-white pixel skull. Base-layer consensus sees valid witness data; Ordinals-aware software supplies the inscription ID, numbering, sat tracking, and rendering convention.

*Why it stands out:* The modern Bitcoin digital-artifact wave began with a deliberately primitive memento mori.

## One Wizard nearly filled a whole block

**Chain context:** 1 FEB 2023 · 3,938,383 BYTES · ZERO TRANSACTION FEE · [Inspect the chain record](https://mempool.space/tx/0301e0480b374b32851a9462db29dc19fe830a7f7d7a88b81612b9d42099c0ae)

Taproot Wizards inscription 652 is a roughly 3.9 MB JPEG. Its transaction weighed 3,938,665 units because witness bytes receive the SegWit discount. Luxor included the zero-fee transaction in its own block.

*Why it stands out:* It made byte size, block weight, miner discretion, and public-mempool fees impossible to confuse.

## Block 840,000 was a halving + land rush

**Chain context:** 20 APR 2024 · 3,050 TRANSACTIONS · 37.626 BTC FEES · [Inspect the chain record](https://mempool.space/block/0000000000000000000320283a032748cef8227873ff4872689bf23f1cda83a5)

The fourth halving cut the subsidy from 6.25 to 3.125 BTC. ViaBTC's block earned about 37.626 BTC in fees amid competition to place early Runes entries and commemorative messages at the exact height.

*Why it stands out:* One block became a subsidy milestone, fee-market stress test, and digital-artifact land rush.

## A publishing script appears to have published itself

**Chain context:** 1 APR 2015 · BLOCK 350,287 · 17,778-BYTE TRANSACTION · [Inspect the chain record](https://mempool.space/tx/1e47936f37e71b98e8bafe51ddc902d59c1318bc556329ba4ab1996981785292)

Peter Todd's proof-of-concept publish-text.py placed padded plaintext in P2SH spending inputs so the Unix strings utility could recover it. A peer-reviewed metadata study found the tool's own Python source in this transaction—apparently uploaded by the tool itself.

*Why it stands out:* It is a blockchain recursion joke: the program explains how to publish text while serving as the text it published.

## Skynet found nihilism—and forgot its domain

**Chain context:** 5 NOV 2013 · BLOCK 268,081 · 926-BYTE TRANSACTION · [Inspect the chain record](https://mempool.space/tx/61e26d407c17e8ee33a8b166c78f78c53cdcdc0078ae1f9405e6583cfb90eaf4)

One transaction carries a radio anecdote and a Terminator parody. Skynet becomes self-aware, discovers nihilism, may switch itself off—and later loses its domain name.

*Why it stands out:* The machine apocalypse ends in existential despair and an expired registration.

## Bitcoin keeps 1,000+ digits of an endless number

**Chain context:** 7 DEC 2013 · BLOCK 273,522 · ATOMSEA / EMBII ROOT · [Inspect the chain record](https://mempool.space/tx/70fd289901bae0409f27237506c330588d917716944c6359a8711b0ad6b4ce76)

An ordered data chain reconstructs more than one thousand decimal digits of π. The root is merely the doorway: a decoder must follow and reassemble the linked payload chunks.

*Why it stands out:* Bitcoin stored a permanently incomplete excerpt of a number that never ends.

## A transaction became a poetry journal

**Chain context:** 1 JUL 2014 · BLOCK 308,775 · 4,476 BYTES · [Inspect the chain record](https://mempool.space/tx/e3e37ed5c1de2631c147bd39429e42ff634e95b7d72423bc32d6c6b9d8eef8ee)

An anonymous first journal entry introduces old poetry produced with ciphers. The transaction behaves like the opening page of a personal literary notebook made deliberately difficult to erase.

*Why it stands out:* A financial ledger became a one-entry magazine for cipher-generated poems.

## A job application went on-chain—and got no reply

**Chain context:** 1 DEC 2014 · BLOCK 332,467 · 3,081 BYTES · [Inspect the chain record](https://mempool.space/tx/604f17dfdb5a88fc072bd2bcf53436087c899051241e519af7241dc0037d3df6)

A long cover letter praises Hive's Bitcoin products and closes “Sincerely, Tim Daubenschuetz.” A later first-person comment says the company never answered.

*Why it stands out:* Even the costliest possible delivery receipt cannot force a recruiter to respond.

## The Arecibo message was sent again—to Bitcoin

**Chain context:** 7 JAN 2015 · BLOCK 337,874 · 1,679-BIT PATTERN · [Inspect the chain record](https://mempool.space/tx/c6d2e535cd2ba4659e954a61198c66fd98c60f6475cf8ff92a404f3fe3a16c4b)

The 1974 radio message encoded numbers, chemistry, DNA, a human, the Solar System, and a telescope. Four decades later, its bit pattern and an SVG visualization were republished through Bitcoin.

*Why it stands out:* A message for hypothetical aliens became one for hypothetical chain archaeologists.

## A Super Mario coin became a Bitcoin coin

**Chain context:** 1 MAR 2015 · BLOCK 345,745 · 951-BYTE TRANSACTION · [Inspect the chain record](https://mempool.space/tx/bf7ef3216ae09f8252c76e7d0031bc4aa131a23a6900f8371c44ffde7957c8da)

An HTML image tag contains a base64-encoded PNG. Decoding it reveals a 16 × 16 coin sprite associated with Super Mario—an almost perfect visual pun for Bitcoin.

*Why it stands out:* The blockchain's “coin” is literally represented by a video-game coin.

## Mr. Spock speaks from a pre-Ordinals MP3 chain

**Chain context:** 2 MAR 2015 · BLOCK 345,858 · ATOMSEA / EMBII ROOT · [Inspect the chain record](https://mempool.space/tx/1bc87dbff1ff5831287f62ac7cf95579794e4386688479bab66174963f9a4a0c)

A linked media chain reconstructs Spock_Live_Long_And_Prosper.mp3. Pre-Ordinals experiments were already carrying sound, not only text and images.

*Why it stands out:* A fictional alien blessing became archival audio one week after Nimoy's death.

## Wedding vows were GPG-signed, then put on-chain

**Chain context:** 12 APR 2015 · BLOCK 351,836 · OPENPGP SIGNED TEXT · [Inspect the chain record](https://mempool.space/tx/b55c3312ceeeb4ab422b658f5f4d5884775a498ddde6a527fca7b67752e1b044)

The message names Zachary Thomas Smith and Jenna Marie Vaziri and wraps their vows in an OpenPGP signed-message format: personal promise, digital signature, and timestamped publication.

*Why it stands out:* “Forever” appears as marital language, a signature, and an append-only ledger.

## A short story shipped with a Bitcoin tip jar

**Chain context:** 11 JUL 2015 · BLOCK 364,852 · TWO-PART STORY · [Inspect the chain record](https://mempool.space/tx/3405f441f0d3acd8580d261d58e5a14d7638d0ee29200e673f496198d231edd7)

How to Play Chinese Hats opens in a smoky, windowless room where gentlemen shuffle traditional hats. The byline “Ren” includes a Bitcoin address that later received one 0.0259 BTC tip.

*Why it stands out:* Blockchain publishing briefly became a fiction magazine—and somebody tipped.

## TrueCrypt 7.1a checksums were “set in stone”

**Chain context:** 19 JUL 2015 · BLOCK 366,067 · 7,772 BYTES · [Inspect the chain record](https://mempool.space/tx/0f96b2f6e3c4f4b6319efbafd2e7148d507b260b4d7914766e79aec7d9ac9574)

After TrueCrypt's abrupt shutdown, one publisher recorded file sizes and digests for the final widely trusted release, intending to help future users verify surviving copies.

*Why it stands out:* A discontinued encryption tool received a checksum tombstone in another cryptosystem.

## A Bitcoin root pointed toward a Pac-Man page

**Chain context:** 8 MAR 2016 · BLOCK 401,657 · CROSS-CHAIN POINTER · [Inspect the chain record](https://mempool.space/tx/03cb74f270d498302d4dd9cbe82c090d801c8840ab6cb26b71d862489b981db8)

The Bitcoin transaction carries signed AtomSea/EMBII metadata and a content link whose chain marker is POT. The playable HTML and JavaScript belong to the referenced Potcoin-side chain, so Bitcoin proves the root record—not the complete game payload.

*Why it stands out:* The oddity is the boundary: one ledger can notarize a doorway into content carried somewhere else.

## Someone wrote to future artificial intelligence

**Chain context:** 25 MAR 2016 · BLOCK 404,143 · 7,468 BYTES · [Inspect the chain record](https://mempool.space/tx/206a0edb11ba0677248709d9bc5210b35e8a03710d9bb19c6f1e4e254bf21f5e)

A long letter begins “Dear Artificial Intelligence,” and treats a future machine mind as the eventual reader. The chain proves a human in 2016 paid to leave the bytes—not that its predictions are true.

*Why it stands out:* The intended reader of this time capsule may be software rather than a person.

## A gas-mask self-portrait ends with “Hi mom!”

**Chain context:** 16 JUN 2016 · BLOCK 416,527 · JPEG IN SCRIPT DATA · [Inspect the chain record](https://mempool.space/tx/c206e8fff656f07b27dac831ef9b956792bae4e76a2cb43f14f49f0298bf2c2f)

A muscular man in a gas mask appears beside “Hyena was here” and “Hi mom! I love you.” Reverse-link evidence connects the 1Hyena profile to Cryptograffiti creator Erich Erstu.

*Why it stands out:* An ominous cyberpunk portrait closes with the most ordinary message home.

## They Live became an Ethereum grave-dance taunt

**Chain context:** 18 JUN 2016 · BLOCK 416,896 · 128 × 128 JPEG · [Inspect the chain record](https://mempool.space/tx/83df1e5ecc1c7ac455d2855e15cff8fa5771afe2ad1796c8b6b1a8e910e829c4)

A still from John Carpenter's They Live rewrites its one-liner: the speaker came to chew bubble gum and dance on Ethereum's grave—and is out of bubble gum.

*Why it stands out:* An action-movie threat became permanent protocol tribalism.

## A wedding portrait carries a classical Chinese poem

**Chain context:** 20 JUN 2016 · BLOCK 417,131 · 71,594-BYTE JPEG · [Inspect the chain record](https://mempool.space/tx/609d5e0f968c0ab7abc2be21468cfd552483d38b08e6df23d27766eb61b9be3c)

A couple in traditional clothing stands before mountains. Four seven-character lines form a qijue-style poem, while metadata supplies an English rendering about a gemstone enduring like constellations.

*Why it stands out:* A private wedding keepsake and bilingual poem became one very public transaction.

## Superbuffo claimed a blockchain comedy first

**Chain context:** 21 JUN 2016 · BLOCK 417,354 · 46,365-BYTE FILE · [Inspect the chain record](https://mempool.space/tx/6240f61bbaeac66cd623e921a153addaf5f379a996f2de0f0c6506d628fe3812)

A portrait file declares “Superbuffo the first comedian on the blockchain.” Later web traces associate the persona with performer Toni Caradonna, but the transaction alone does not establish that identity.

*Why it stands out:* The chain has a self-appointed first comedian—and the fee may be the punchline.

## The second halving block opened with a love note

**Chain context:** 9 JUL 2016 · BLOCK 420,000 · SUBSIDY 25 → 12.5 BTC · [Inspect the chain record](https://mempool.space/block/000000000000000002cce816c0ab2c5c269cb081896b7dcb34b8422d6b74ffa1)

The first block after Bitcoin's second halving begins with “Chandler Guo loves YangYang Jin.” A monetary-supply milestone and a personal declaration share one coinbase input.

*Why it stands out:* A major issuance milestone began with five words of affection.

## A yellow street robot received coordinates and immortality

**Chain context:** 2014 CONTENT ROOT · 2017 LINK / INDEX TRANSACTION · [Inspect the chain record](https://mempool.space/tx/4cbb32cd27b5b5edc12d3559bdffc1355ac2a210463d5cfaadc7ce9b06675b2b)

A Chicago street-art photo records N 41.880778, E −87.629210 and predicts the physical robot will be paved over or removed. A later 2017 transaction indexes an earlier 2014 content chain.

*Why it stands out:* Ephemeral street art was archived with a map back to where it would vanish.

## A manifesto insists Tau is better than Pi

**Chain context:** 11 MAR 2017 · BLOCK 456,806 · 1,256-BYTE TRANSACTION · [Inspect the chain record](https://mempool.space/tx/e450166eba552202fb6984867f2b851e2399c5a0ae05026bf6b056176491ec5d)

A transaction input carries a long argument for τ = 2π as the universal circle constant. Its author prefers a constant equal to one full turn rather than half a turn.

*Why it stands out:* After storing π, someone paid Bitcoin to argue that π was the wrong choice.

## Tank Man crossed another censorship boundary

**Chain context:** 21 MAR 2017 · BLOCK 458,238 · 40,620 BYTES · [Inspect the chain record](https://mempool.space/tx/ca4f11131eca6b4d61daf707a470cfccd1ef3d80a6f8b70f1f07616b451ca64e)

A transaction reconstructs the famous photograph of the unidentified man before a tank column during the 1989 Tiananmen crackdown—a symbol repeatedly censored in China.

*Why it stands out:* A censorship symbol was copied into a system built to resist selective deletion.

## Mr. Burns says: “You're here forever”

**Chain context:** 5 APR 2017 · BLOCK 460,435 · 39,544-BYTE IMAGE · [Inspect the chain record](https://mempool.space/tx/94e319d09fc236fb9d7a24e60af8f47ed41ca3cc01e9950c925d806153ed8aa3)

Input scripts reconstruct a Simpsons still in which Mr. Burns points to “Don't forget, you're here forever.” In its new storage context, the workplace joke becomes literal.

*Why it stands out:* The caption accidentally describes the image's own persistence.

## A college JPEG included its own reconstruction hint

**Chain context:** 7 JUL 2017 · BLOCK 474,586 · 78,384-BYTE REVEAL · [Inspect the chain record](https://mempool.space/tx/033d185d1a04c4bd6de9bb23985f8c15aa46234206ad29101c31f4b33f1a0e49)

A two-stage P2SH construction stores Augustana College's Old Main. Beside the bytes is a field note: reconstruct the JPEG using data preceding the redeem scripts.

*Why it stands out:* The photograph arrived with its own archaeological instruction label.

## A mistaken payment produced an on-chain refund plea

**Chain context:** 18 AUG 2017 · BLOCK 481,032 · CROSSCHAIN ERROR NOTE · [Inspect the chain record](https://mempool.space/tx/0f25e23b7b59fde67d8b2d41b749e4f89fd1ff8061aa0ddac8c27c8230167e35)

A message says a Crosschain transaction was sent in error, cites the mistaken payment, and asks for return to a Bitcoin address. The observed return address showed no repayment at review time.

*Why it stands out:* An irreversible payment created a note slipped under the recipient's door.

## The Starry Night entered SegWit before Ordinals

**Chain context:** 31 MAY 2021 · BLOCK 685,647 · 6,505 WEIGHT UNITS · [Inspect the chain record](https://mempool.space/tx/225ed8bc432d37cf434f80717286fd5671f676f12b573294db72a2a8f9b1e7ba)

A SegWit transaction carries a small JPEG of Vincent van Gogh's The Starry Night about twenty months before Ordinals launched. It is witness-data archaeology, not an Ordinals inscription.

*Why it stands out:* Art was already hiding in witness data before Ordinals named the practice.

## “Running Bitcoin” became Hal Finney's epitaph

**Chain context:** 6 DEC 2024 · BLOCK 873,447 · CANONICAL TXID VERIFIED · [Inspect the chain record](https://mempool.space/tx/ea38c62294fa9a5c6ccbfe4c307bd9133a8dc407181b69fa092a1781cbf870bb)

An OP_RETURN says: “In loving memory of Hal Finney: Running Bitcoin and funding ALS research.” It sends his famous 2009 phrase back into the ledger he helped test.

*Why it stands out:* One of Bitcoin's first human stories received an explicit on-chain epitaph.

## One sermon occupied 8,620 transactions

**Chain context:** 8–10 JUL 2025 · BLOCKS 904,530–904,881 · ≈673 KB · [Inspect the chain record](https://mempool.space/tx/b486b14d501eeadcd7e31cefea9771c769552ad705dc4bbab6a797fc4b3086f9)

A publisher split continuous religious text and personal testimony across 8,620 sequence-tagged OP_RETURN transactions. The linked record is the first fragment rather than proof of the complete aggregate.

*Why it stands out:* A field suited to a sentence was brute-forced into a multi-day book.
