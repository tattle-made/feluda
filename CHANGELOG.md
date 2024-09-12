# CHANGELOG



## v0.8.0 (2024-09-12)

### Chore

* chore: updating vid vec rep resenet packages ([`9f212c2`](https://github.com/tattle-made/feluda/commit/9f212c2d21cb7ad33a41330f203dab3d41f04d69))

* chore: updating audio vec embedding pacakges ([`a41f996`](https://github.com/tattle-made/feluda/commit/a41f996f40af1b5f9c70786ee376c6a5f2348b32))

* chore: updating audio vec embedding pacakges ([`6e50e06`](https://github.com/tattle-made/feluda/commit/6e50e0683702cc9549773ab6bffa742a43105835))

* chore: fix conflict in updating requirements packages ([`acf1a56`](https://github.com/tattle-made/feluda/commit/acf1a564d872c26575f0d23abe5a7a7b56df8c94))

* chore: updating requirements packages ([`5390073`](https://github.com/tattle-made/feluda/commit/5390073e3a848e0984ef6049d1500991d27583aa))

* chore: fix ruff lint warnings ([`5f73898`](https://github.com/tattle-made/feluda/commit/5f738980d18eb9572d61b26aaf7a6f23ac016aaa))

* chore: add error handling to clustering and reduction operations ([`ba01287`](https://github.com/tattle-made/feluda/commit/ba01287cd7cbb175b516874fcc489e5b0261ebc7))

* chore: hardcode perplexity value for t-SNE ([`60315b5`](https://github.com/tattle-made/feluda/commit/60315b5fe96e445831c8c84641b8eb95f2d0e701))

* chore: change operator name to be more verbose

Signed-off-by: Snehil Shah &lt;snehilshah.989@gmail.com&gt; ([`45bef72`](https://github.com/tattle-made/feluda/commit/45bef72d74617bff5915429e3802fc88b9ed595a))

* chore: remove obsolete `print` statement

Signed-off-by: Snehil Shah &lt;snehilshah.989@gmail.com&gt; ([`92d02e2`](https://github.com/tattle-made/feluda/commit/92d02e219ecb0844de261b35fa2801adca139f04))

* chore: remove the file after the operation has ended

Signed-off-by: Snehil Shah &lt;snehilshah.989@gmail.com&gt; ([`4a384f5`](https://github.com/tattle-made/feluda/commit/4a384f57b6f4daa41861162898415fa981dc73e0))

* chore: removing docs gatsby website ([`03f5ac0`](https://github.com/tattle-made/feluda/commit/03f5ac078952851fdf17954484f34eccd066ca72))

### Ci

* ci: fix trivy github action ([`a5d4df8`](https://github.com/tattle-made/feluda/commit/a5d4df8d2e5f0b9b1654134557509df0a45c4583))

* ci: update dependabot yml file ([`8a6b007`](https://github.com/tattle-made/feluda/commit/8a6b007235c957e76e369bc3d2346a45f50aa337))

### Feature

* feat: add config

Signed-off-by: Snehil Shah &lt;snehilshah.989@gmail.com&gt; ([`73731ec`](https://github.com/tattle-made/feluda/commit/73731eceaad6e33c78052654012b1927e3682e5d))

* feat: add dimensionality reduction operator ([`2caf4a4`](https://github.com/tattle-made/feluda/commit/2caf4a4398383ae95731ce167c3d7d5391a49284))

* feat: improve exception handling and logic

Co-authored-by: Chaithanya512 &lt;chay5522kalyan@gmail.com&gt;
Signed-off-by: Snehil Shah &lt;snehilshah.989@gmail.com&gt; ([`5756a59`](https://github.com/tattle-made/feluda/commit/5756a59d2a8f2e7395ff566f07213fbb6bb75bcd))

* feat: add `cluster_embeddings` operator

Signed-off-by: Snehil Shah &lt;snehilshah.989@gmail.com&gt; ([`4e08e35`](https://github.com/tattle-made/feluda/commit/4e08e35309c415b1bae0f65732d9df635da342a4))

* feat: add audio embedding operator using CLAP model ([`233cfd4`](https://github.com/tattle-made/feluda/commit/233cfd4065f2e43d6cf533ade3002270f02f5eb2))

* feat: add `classify_video` operator

Signed-off-by: Snehil Shah &lt;snehilshah.989@gmail.com&gt; ([`2001dab`](https://github.com/tattle-made/feluda/commit/2001dab2f38b0892b31cb269d85a118d16c0210f))

* feat: add `vid_vec_rep_clip` operator

Signed-off-by: Snehil Shah &lt;snehilshah.989@gmail.com&gt; ([`8874ce5`](https://github.com/tattle-made/feluda/commit/8874ce58d5ee77df7844c6b49ae5180736fee00e))

### Fix

* fix: es_vec test ([`08b3085`](https://github.com/tattle-made/feluda/commit/08b308587029507136cdc4fe68719a1357b84917))

* fix: enable worker support for dimension reductionn ([`89df059`](https://github.com/tattle-made/feluda/commit/89df059b251cd2ed7cddb46e39d60fe2d8b45e48))

* fix: update logic as per clustering spec

Signed-off-by: Snehil Shah &lt;snehilshah.989@gmail.com&gt; ([`0bea260`](https://github.com/tattle-made/feluda/commit/0bea260224c49cb6c2e0f0a47832789ff8b6591b))

* fix: correct indentation logic ([`d208d17`](https://github.com/tattle-made/feluda/commit/d208d17ba7f2c2914ca3666f1b25295d50524eab))

* fix: correct naming and add dimension reduction requirements ([`0334a4b`](https://github.com/tattle-made/feluda/commit/0334a4b20a5555c8278ba8fc99c55327c0c27b8b))

### Refactor

* refactor: migrate CLAP operator to Hugging Face Transformers ([`9e5195a`](https://github.com/tattle-made/feluda/commit/9e5195aa8ddf2c86d54333ee6e9c01a5576b32f4))

* refactor: align dimension reduction with feluda interface ([`0acfdb7`](https://github.com/tattle-made/feluda/commit/0acfdb74befae505f20ebf112bb3a58b087ca980))

* refactor: change modality to `video`

Signed-off-by: Snehil Shah &lt;snehilshah.989@gmail.com&gt; ([`a1506ba`](https://github.com/tattle-made/feluda/commit/a1506ba879444458f09f286d34baec94b38c3744))

### Style

* style: prepend newline for clearer output in logs

Signed-off-by: Snehil Shah &lt;snehilshah.989@gmail.com&gt; ([`bacafdd`](https://github.com/tattle-made/feluda/commit/bacafdd95142078626e1b996258859f13bbf8d97))

### Test

* test: add payload writer for the worker

Signed-off-by: Snehil Shah &lt;snehilshah.989@gmail.com&gt; ([`57803e0`](https://github.com/tattle-made/feluda/commit/57803e07451e8263544cc8d239f2e95a99c303e0))

### Unknown

* Merge pull request #381 from tattle-made/development

merge dev to main ([`48bfc87`](https://github.com/tattle-made/feluda/commit/48bfc87b813f5a34ea59c7bc9e7d7316000ce1ee))

* Merge pull request #380 from aatmanvaidya/update-fel

Update Packages and Fix minor Issues ([`cf64f4d`](https://github.com/tattle-made/feluda/commit/cf64f4d5ead811883d5012656222a3459cae4f09))

* Merge pull request #379 from Snehil-Shah/worker

worker for clustering media ([`4abae4d`](https://github.com/tattle-made/feluda/commit/4abae4dff4cd0d50c20eeb152c5a7220d2385923))

* nit: add logs

Signed-off-by: Snehil Shah &lt;snehilshah.989@gmail.com&gt; ([`1ba6de1`](https://github.com/tattle-made/feluda/commit/1ba6de164563dd086ab4797586a44c62770d8dd1))

* draft: implement initial clustering worker ([`7129ac3`](https://github.com/tattle-made/feluda/commit/7129ac3ee76993bd97eb10ac2df6ff703da86dcb))

* init: add Dockerfile for worker

Signed-off-by: Snehil Shah &lt;snehilshah.989@gmail.com&gt; ([`777994b`](https://github.com/tattle-made/feluda/commit/777994b597b1554a7bbfb77dd3eed8967a3757a5))

* Merge pull request #375 from Snehil-Shah/clustering

[81] - add operator to cluster embeddings ([`1da1c27`](https://github.com/tattle-made/feluda/commit/1da1c275fe840327c88623ef8d6b968338ebfc89))

* Merge pull request #376 from Chaithanya512/dim-reduction-operator

feat: add dimensionality reduction operator ([`cb76d85`](https://github.com/tattle-made/feluda/commit/cb76d85c0cb1e32295b0cf1e39d765bf4b1efb0b))

* Merge pull request #372 from Chaithanya512/audio_vec_emb_clap

feat: audio embedding operator using CLAP model ([`faa9727`](https://github.com/tattle-made/feluda/commit/faa9727eec8c4639ea61615c69c006384dbb5665))

* Merge pull request #370 from Snehil-Shah/classify-video

[81] - add operator to classify videos using a zero-shot approach ([`91f604b`](https://github.com/tattle-made/feluda/commit/91f604b5e04e109645c0e55f1c691ddd7d9fb681))

* Merge pull request #369 from Snehil-Shah/vid_vec_rep_clip

[81] - add operator to encode videos into vector embeddings using `CLIP-ViT-B-32` ([`c5f09de`](https://github.com/tattle-made/feluda/commit/c5f09de7dba47eed1ef8efe4eae1cf5d7c16def5))

* Merge pull request #367 from aatmanvaidya/remove-docs

chore: removing docs gatsby website ([`2b9275a`](https://github.com/tattle-made/feluda/commit/2b9275a134677a1338dfbd5f7c9fcd9922c7b447))


## v0.7.2 (2024-05-28)

### Fix

* fix: Updated pr-security workflow
fix: Removed ignored vulnerabilities that were fixed ([`fe9c26a`](https://github.com/tattle-made/feluda/commit/fe9c26a3e61babbae170d855196a4d47e1b45235))

### Unknown

* Merge pull request #344 from tattle-made/hotfix

Hotfix ([`10a277c`](https://github.com/tattle-made/feluda/commit/10a277c96cc382d929e9f2fb21ac0c903abbf3dc))

* Merge pull request #343 from duggalsu/update_pr_security_workflow

Update pr security workflow ([`b26a03c`](https://github.com/tattle-made/feluda/commit/b26a03c3f8697a0e996ea3288ea8f880478d70ce))


## v0.7.1 (2024-05-28)

### Fix

* fix: Updated github action versions to latest ([`44b46ad`](https://github.com/tattle-made/feluda/commit/44b46ad84d4b651a0f4ca264c21eab23d7defd4f))

### Unknown

* Merge pull request #342 from tattle-made/hotfix

Hotfix ([`eecc55f`](https://github.com/tattle-made/feluda/commit/eecc55f07d397142f8980c3cc2fedecd15a186a5))

* Merge pull request #341 from duggalsu/update_scorecard_workflow

Update scorecard workflow ([`b2e2aa8`](https://github.com/tattle-made/feluda/commit/b2e2aa852f3377490f6cebd679706678b89e5c50))


## v0.7.0 (2024-05-28)

### Chore

* chore: update Dockerfile ([`8ca692e`](https://github.com/tattle-made/feluda/commit/8ca692ed39051237a3f1922571f218569a6695e4))

* chore: removing file size limit from vid_vec_rep_resnet ([`22b9f2a`](https://github.com/tattle-made/feluda/commit/22b9f2a9d36ff746572b447910ed2eb32b4d6765))

### Ci

* ci: prod github action for media worker ([`d4bb47f`](https://github.com/tattle-made/feluda/commit/d4bb47fe7e6567b341957c67d6ef34b9732e0394))

### Unknown

* Merge pull request #339 from tattle-made/development

Merge Dev to Main ([`a1c22d3`](https://github.com/tattle-made/feluda/commit/a1c22d38a82e0f46caffec6a0dbfeaa24ca581ed))

* Merge pull request #340 from tattle-made/aatmanvaidya-patch-1

chore: update Dockerfile ([`eb018a8`](https://github.com/tattle-made/feluda/commit/eb018a8dc79bb328952049089d0e0a178e31b261))

* Merge pull request #332 from aatmanvaidya/media-worker-for-es

fix: updating media worker to index videos only ([`e6a8510`](https://github.com/tattle-made/feluda/commit/e6a851062c2cbfe89231a1ea558ec53dd4822f1b))

* Merge pull request #324 from Snehil-Shah/language-detection

feat: add operator to detect language in an audio file ([`acfa3a0`](https://github.com/tattle-made/feluda/commit/acfa3a0b1c3c9d82004e11b524cb10932c6c456e))

* Merge remote-tracking branch &#39;upstream/main&#39; into media-worker-for-es ([`157508b`](https://github.com/tattle-made/feluda/commit/157508bc3a80d452de6ae644cceaa1a5396c487d))


## v0.6.6 (2024-05-24)

### Chore

* chore: fixing ruff lint errors ([`b655e96`](https://github.com/tattle-made/feluda/commit/b655e96c842d7fdd8623bf2655aa3fb5bb86ae0c))

* chore: affix version &amp; generate hashed `requirements.txt` ([`7305560`](https://github.com/tattle-made/feluda/commit/7305560c409ff4bc714c20344e3b0ef087c5080b))

### Documentation

* docs: update module doc ([`14de2fa`](https://github.com/tattle-made/feluda/commit/14de2fab4520583c495e514b31efb7d528d20ed7))

### Feature

* feat: improve speech extraction&#39;s perfomance time ([`d105009`](https://github.com/tattle-made/feluda/commit/d105009835cfa5d934005764313b200dc7c1fa0e))

* feat: add operator for language detection in audio

Signed-off-by: Snehil Shah &lt;snehilshah.989@gmail.com&gt; ([`2744035`](https://github.com/tattle-made/feluda/commit/2744035d27499e98f9b9f21b3188fc4881390d46))

### Fix

* fix: Updated vulnerable requests package ([`4b97299`](https://github.com/tattle-made/feluda/commit/4b97299ba1ba9ff3b1363c3f4d4912443f907413))

* fix: updating media worker to index vidoes only ([`926044d`](https://github.com/tattle-made/feluda/commit/926044da78e20066bf3c4fd0eaced7dab9f99b5f))

* fix: securely handle tmp for storage safety ([`8f3fa52`](https://github.com/tattle-made/feluda/commit/8f3fa526aac5f63a094fc815cb5fa6136cd96b94))

### Test

* test: add case for speech extraction from heterogeneous audio ([`b448a5b`](https://github.com/tattle-made/feluda/commit/b448a5b0d7136ab08cd1ff9d5d0dead8723bbe64))

### Unknown

* Merge pull request #334 from tattle-made/hotfix

Hotfix ([`b9f921a`](https://github.com/tattle-made/feluda/commit/b9f921adf9c1e86ea24089d6ce5aaea29dd33edb))

* Merge pull request #333 from duggalsu/fix_dependabot_20240524

Fix dependabot 20240524 ([`e7704e1`](https://github.com/tattle-made/feluda/commit/e7704e17e3171246cd7426bab6af385aded62c13))

* Regenerated src/requirements.txt ([`e25bd43`](https://github.com/tattle-made/feluda/commit/e25bd43893f034b139bc5d9ce707d531912c3231))


## v0.6.5 (2024-05-10)

### Chore

* chore: removing store from hash worker config ([`9f71faa`](https://github.com/tattle-made/feluda/commit/9f71faa723c559e9fd8b1592b77cde3b9ecf4788))

### Fix

* fix: adding store check in hash worker ([`73157e1`](https://github.com/tattle-made/feluda/commit/73157e197efc59a949bc02a4895b057fcb43f908))

### Unknown

* Merge pull request #309 from tattle-made/hotfix

Hotfix ([`f21e2e6`](https://github.com/tattle-made/feluda/commit/f21e2e623038ec019ae8a7c17c437032eff6b9a9))

* Merge pull request #308 from aatmanvaidya/hash-fix

fix: adding store check in hash worker ([`4af10d9`](https://github.com/tattle-made/feluda/commit/4af10d9aeb549e0e64e624c9c131ea6eac27d250))

* Merge pull request #307 from tattle-made/hotfix

Hotfix ([`8723337`](https://github.com/tattle-made/feluda/commit/8723337ea173ab3a9e0e3ef1acf07af53908cb00))

* Merge pull request #306 from aatmanvaidya/hash-config-hotfix

chore: removing store from hash worker config ([`75c4a78`](https://github.com/tattle-made/feluda/commit/75c4a78e86312c5a51800d4f639402499ef4336d))


## v0.6.4 (2024-05-08)

### Fix

* fix: Update packages to fix vulnerabilities ([`d222f9c`](https://github.com/tattle-made/feluda/commit/d222f9cfbf0197f331f43e02d7d5256a2f66eee8))

### Unknown

* Merge pull request #305 from tattle-made/hotfix

Hotfix ([`2d1bb77`](https://github.com/tattle-made/feluda/commit/2d1bb77bb70c7806dc4f6b0e7f92541da3c49436))

* Merge pull request #304 from duggalsu/fix_dependabot_20240507

Fix dependabot issues ([`97cc70d`](https://github.com/tattle-made/feluda/commit/97cc70d647df1c699436134967b2c653226190fe))


## v0.6.3 (2024-05-07)

### Fix

* fix: config-server structure ([`831cf54`](https://github.com/tattle-made/feluda/commit/831cf5428fdae43467e32ad504497b5d67dfbf84))

### Unknown

* Merge pull request #303 from tattle-made/hotfix

Hotfix ([`ce0f0e1`](https://github.com/tattle-made/feluda/commit/ce0f0e1efacba89c053a6136f5de2a9ac85f579f))

* Merge pull request #302 from aatmanvaidya/config-fix

fix: config-server structure ([`ed1c62b`](https://github.com/tattle-made/feluda/commit/ed1c62b679f628b89cbeb86b87eac78354b88a4b))


## v0.6.2 (2024-05-06)

### Fix

* fix: adding base requirements to media worker dockerfiles ([`bbddf70`](https://github.com/tattle-made/feluda/commit/bbddf704fb95ffaa900e7a9530648edb6834a286))

### Unknown

* Merge pull request #293 from tattle-made/hotfix

Hotfix ([`31abc9d`](https://github.com/tattle-made/feluda/commit/31abc9d47f8dd2d4dba80efac780bbdccf82334d))

* Merge pull request #292 from aatmanvaidya/pinned-dep-fix

fix: adding base requirements to media worker dockerfiles ([`bd95984`](https://github.com/tattle-made/feluda/commit/bd959847a59035f177e5aafc2d7b52ed9b321dbc))


## v0.6.1 (2024-05-06)

### Fix

* fix: tqdm vulnerable version update ([`841a748`](https://github.com/tattle-made/feluda/commit/841a748aa5d87afa4df2ca225107100b422d50b5))

### Unknown

* Merge pull request #291 from tattle-made/hotfix

Hotfix ([`4ed81ab`](https://github.com/tattle-made/feluda/commit/4ed81abf1d887743bb84687da109f67af4b6a3ca))

* Merge pull request #290 from duggalsu/fix_dependabot_20240506

Fix dependabot issues ([`444a06f`](https://github.com/tattle-made/feluda/commit/444a06fc19892fc8b5d675d0221d7f79c1ea95c3))


## v0.6.0 (2024-05-01)

### Chore

* chore: fixing merge conflicts ([`4ce050e`](https://github.com/tattle-made/feluda/commit/4ce050ed0338fcf60680092a5d6fee656f81fb3a))

### Unknown

* Merge pull request #286 from tattle-made/development

chore: merging development to main ([`bba03e4`](https://github.com/tattle-made/feluda/commit/bba03e4f6588ac1981ccb74cf048968e4760d98f))

* Merge pull request #285 from aatmanvaidya/dev-2

chore: fixing merge conflicts ([`6239cef`](https://github.com/tattle-made/feluda/commit/6239cefa03fec6e74806a2511faaaff64ec1b747))


## v0.5.4 (2024-04-30)

### Chore

* chore: sending ack on exception instead of nack ([`f6d9258`](https://github.com/tattle-made/feluda/commit/f6d9258eeedaa730365a7faea0ff517c78b20357))

* chore: if statement checks for store in config inside media worker ([`435cf80`](https://github.com/tattle-made/feluda/commit/435cf800daddbdc5ed1e7009688de7c5f8cfca74))

* chore: updating hash worker config ([`059d878`](https://github.com/tattle-made/feluda/commit/059d87801e4605f48e40e44c8548e2d1225deafc))

* chore: adding init files for hash and media worker ([`a508c5a`](https://github.com/tattle-made/feluda/commit/a508c5a1386f9f6a3bd1102ae4be5e514555d7ff))

* chore: fixing ruff lint error ([`82f85a6`](https://github.com/tattle-made/feluda/commit/82f85a60709fb30faaddb53becce99881c0ee224))

* chore: deleting empty query.py file in store ([`8cf33fc`](https://github.com/tattle-made/feluda/commit/8cf33fccea43d73ecffed3193f6c55edbc71e3ae))

* chore: fixing ruff lint error ([`8b920d5`](https://github.com/tattle-made/feluda/commit/8b920d548a002ade0c5c0217fb0759507a553172))

* chore: deleting media test file ([`9ad98f7`](https://github.com/tattle-made/feluda/commit/9ad98f7f8d2f8b59878c206909fc164701489647))

### Ci

* ci: media worker staging workflow ([`a4280f4`](https://github.com/tattle-made/feluda/commit/a4280f49257b83b06731a130413a95e9545ef539))

* ci: Added npm ci for pinned package installation
- Added setup node version action ([`60c47e8`](https://github.com/tattle-made/feluda/commit/60c47e84171f88aa3e3df890c2f19b4af34dc01b))

* ci: Added using ruff action for CI linting ([`246c6cd`](https://github.com/tattle-made/feluda/commit/246c6cdd50ff7f6cd09ffbc65e7686e4f9553e20))

* ci: Fix bandit to run from single workflow
- Added bandit.yml to run on PR
- Disabled bandit from pr-security.yml ([`692503e`](https://github.com/tattle-made/feluda/commit/692503ecc328b9860905ef14cd295879d6044d3a))

### Fix

* fix: Fixed dependabot issues
- Updated idna package
- Updated transformers package
- Updated torch and torchvision for python 3.12 compatibility ([`d027dfe`](https://github.com/tattle-made/feluda/commit/d027dfe90ce33b2a8be531bafdd21959a60f1a2b))

* fix: hash worker relies more on core feluda ([`d8aed50`](https://github.com/tattle-made/feluda/commit/d8aed50b4af1f9cfc9dbbac3894a92c80bc96902))

* fix: hash payload writer can send audio/video both ([`502ad4e`](https://github.com/tattle-made/feluda/commit/502ad4e8413641002f17b1f33966d75ca483cb8d))

* fix: sending crc value to report queue ([`a89990e`](https://github.com/tattle-made/feluda/commit/a89990ebe76b8cc507a9eefd1101c1f83537a9c7))

* fix: making store component init more lean ([`3a63883`](https://github.com/tattle-made/feluda/commit/3a63883bf0e52a15092f377c946ad81e733b5586))

* fix: media worker relies more on core feluda ([`0389a3a`](https://github.com/tattle-made/feluda/commit/0389a3af3c412f7bc45f44dcc661253b37fb90ed))

* fix: store can init all components properly ([`9b5a6d9`](https://github.com/tattle-made/feluda/commit/9b5a6d9c84e60b02284b34d612d03dcc4aba14d1))

* fix: store init can start postgresql ([`d9d1cb1`](https://github.com/tattle-made/feluda/commit/d9d1cb120c1391123674d593f9c71911dd292934))

* fix: feluda core supports amazom mq ([`91783af`](https://github.com/tattle-made/feluda/commit/91783af357fbcfe1ccfc4e1e27cf976666c00d67))

* fix: Updated vulnerable pillow dependency in requirements ([`2c60f67`](https://github.com/tattle-made/feluda/commit/2c60f67e8c8fe2f95405386b2df0b7405c8f4965))

* fix: Add pinned dev requirements
- Added dev requirements for feluda core, video and audio benchmark
- Fixed video benchmark not working without new boto3 dependency
- Fixed audio benchmark not working without new wget dependency ([`293d970`](https://github.com/tattle-made/feluda/commit/293d97093f9fe04ac3c20b60125d6190eb4e2a52))

* fix: Added pinned pip package
- Added base requirements.in with pip
- Created base requirements.txt with pip pinned by hash
- Recreated requirements.txt with --allow-unsafe to get correct setuptools
- Updated feluda core dockerfile to install pip using base requirements
- Updated ci test dockerfile to install pip using base requirements
- Updated all benchmark dockerfiles to install pip using base requirements
- Updated all worker dockerfiles to install pip using base requirements
- Updated readme pip install and pip-compile commands ([`05e23b2`](https://github.com/tattle-made/feluda/commit/05e23b24101e5e4a937daa0e6399583004203286))

* fix: adding contextmanager for hash worker ([`312ab3f`](https://github.com/tattle-made/feluda/commit/312ab3fd04046f6eb9fd157c75bf06a419bafdcb))

* fix: audio factory supports s3 download ([`9834490`](https://github.com/tattle-made/feluda/commit/9834490a316aa2a97994f04939bf32f65b8bd12d))

### Refactor

* refactor: updating config structure for store ([`a2252f6`](https://github.com/tattle-made/feluda/commit/a2252f673b6197740839b5d1d59058024aa4214a))

* refactor: s3 download to a new file ([`83ed5cf`](https://github.com/tattle-made/feluda/commit/83ed5cf33ba44006a91259e9b924769b0fdee777))

### Unknown

* Merge pull request #284 from tattle-made/hotfix

Hotfix ([`9d679c0`](https://github.com/tattle-made/feluda/commit/9d679c021e955082bc280d80aa96c15b6b10daff))

* Merge pull request #283 from duggalsu/fix_dependabot_20240430

Fixed dependabot issues ([`1319f89`](https://github.com/tattle-made/feluda/commit/1319f89e87f7ec5abdfd8bd5dfc34b752843f1c0))

* - Added ignore vuln until fix issued ([`9da6bc8`](https://github.com/tattle-made/feluda/commit/9da6bc827f94282399231b9ad1857feb244807ae))

* Merge pull request #275 from aatmanvaidya/ack-fix

chore: sending ack on exception instead of nack ([`0b93759`](https://github.com/tattle-made/feluda/commit/0b937598c87a68433154b6adcbd1278f1f469671))

* Merge pull request #261 from aatmanvaidya/hash-worker-fix

fix: hash worker relies more on core feluda ([`cbf1349`](https://github.com/tattle-made/feluda/commit/cbf13499e6f8a83f8da2ba603197d9122f980941))

* Merge pull request #250 from aatmanvaidya/media-worker

feat: media worker ([`0d97313`](https://github.com/tattle-made/feluda/commit/0d9731386387afda7e1b3e695a1776c55e663f0f))

* - Test inverted ternary operator ([`c7e3e05`](https://github.com/tattle-made/feluda/commit/c7e3e052d94027f3f65602a5438522cfead0ccd2))

* - Modify env settings ([`0e2a13b`](https://github.com/tattle-made/feluda/commit/0e2a13b22b332dea98d09ca328a25e685e9875ef))

* - Test switch conditional values ([`f05fbea`](https://github.com/tattle-made/feluda/commit/f05fbea9f1672acc64e987650be7bfb6b27450b2))

* - Set conditional falsy and truthy values ([`6a1e908`](https://github.com/tattle-made/feluda/commit/6a1e90838b2e26af981a6ee344b72a4e259b40a0))

* - Fix env var boolean setting ([`f80d81e`](https://github.com/tattle-made/feluda/commit/f80d81eb951d68be59201408591552afdfe592de))

* - Added conditional exit_zero for bandit ([`41036ad`](https://github.com/tattle-made/feluda/commit/41036adebe19c085beaad9bec865f52cb0dc4553))


## v0.5.3 (2024-04-04)

### Chore

* chore: amazon mq send_message lint fix ([`063096c`](https://github.com/tattle-made/feluda/commit/063096cecf0b980d1f95482fc189a7825c8ac917))

* chore: adding else condition of media_type ([`4e6e4eb`](https://github.com/tattle-made/feluda/commit/4e6e4eb6c7c66a299bfcb43dabaeee36d825acbb))

* chore: media_type is command line arg in payload writer ([`9d0fa4e`](https://github.com/tattle-made/feluda/commit/9d0fa4eaf2094201a15ee18c1c8c96d4c9ef9d4c))

* chore: store check ([`2df0db6`](https://github.com/tattle-made/feluda/commit/2df0db66cc090cb4dce52deb632092d9168dd4e4))

### Feature

* feat: media worker supports amazon mq ([`8b92b7f`](https://github.com/tattle-made/feluda/commit/8b92b7fb19daefa83a80c263771dea29c3001417))

* feat: Amazon MQ ([`766b805`](https://github.com/tattle-made/feluda/commit/766b8050e86e4eee23c10bf634b0c72e14091314))

* feat: media worker supports audio ([`b92a4d4`](https://github.com/tattle-made/feluda/commit/b92a4d47b47abe3f6335e2011c5f9d760c12d6e8))

* feat: media worker supports video ([`ffba9cd`](https://github.com/tattle-made/feluda/commit/ffba9cda73d4ec6baabbced19409d5dbdb33e7c4))

### Fix

* fix: Updated vulnerable pillow dependency in requirements ([`efd1be8`](https://github.com/tattle-made/feluda/commit/efd1be8bf979d27383e3c7cad2b11a26003ede39))

* fix: setting up payload for audio ([`3a87ce0`](https://github.com/tattle-made/feluda/commit/3a87ce03a3d7d21aa7f0a60a960d28516a7799a8))

* fix: postgres media worker table ([`dd974d2`](https://github.com/tattle-made/feluda/commit/dd974d2837a0b01301f1d66933d99a3f66fcd581))

* fix: media factory audio function update &amp; setting up media worker ([`2e0fda5`](https://github.com/tattle-made/feluda/commit/2e0fda53bf28ea7d652b60075a99ed6cdeb0b2b5))

### Refactor

* refactor: config supports postgres &amp; feat: setting up media payload writer ([`f43f205`](https://github.com/tattle-made/feluda/commit/f43f2057c695425f6c9fc1fc552910a85f7f1d79))

### Unknown

* Merge pull request #257 from tattle-made/hotfix

Hotfix ([`67ac03a`](https://github.com/tattle-made/feluda/commit/67ac03aba15a1f7dbad0641f9539cec09a9b7bdb))

* Merge pull request #256 from duggalsu/update_pillow

Update pillow ([`44b0f88`](https://github.com/tattle-made/feluda/commit/44b0f88e4de6d566bbb6ed8fb6ab0a0db0fe5ec4))


## v0.5.2 (2024-03-23)

### Ci

* ci: Added npm ci for pinned package installation
- Added setup node version action ([`fd4a8f1`](https://github.com/tattle-made/feluda/commit/fd4a8f10d85aa2688589215a106224bfc7aead68))

* ci: Added using ruff action for CI linting ([`ed89995`](https://github.com/tattle-made/feluda/commit/ed89995589dc55b2a251b3c49696c303891d17cf))

### Fix

* fix: Add pinned dev requirements
- Added dev requirements for feluda core, video and audio benchmark
- Fixed video benchmark not working without new boto3 dependency
- Fixed audio benchmark not working without new wget dependency ([`d974e7e`](https://github.com/tattle-made/feluda/commit/d974e7e0ff262e46a779add1e4f1aeaef4e70f25))

### Unknown

* Merge pull request #244 from tattle-made/hotfix

Hotfix ([`7bae56d`](https://github.com/tattle-made/feluda/commit/7bae56d6cbcf7896bdfe0c79d9e1e76869d04c3d))

* Merge pull request #243 from duggalsu/add_dev_requirements

Add dev requirements ([`aa2c09f`](https://github.com/tattle-made/feluda/commit/aa2c09f9d9607880e3e9eb1e418aa5044294c960))

* Merge pull request #242 from tattle-made/hotfix

Hotfix ([`efb06e5`](https://github.com/tattle-made/feluda/commit/efb06e57791e47b27303e0419307f8b8236669fb))

* Merge pull request #241 from duggalsu/use_npm_pinned

Use npm pinned ([`52a4bbf`](https://github.com/tattle-made/feluda/commit/52a4bbf4e7f24936ee8ed1703fbe806b93da62c9))

* Merge pull request #240 from duggalsu/use_ci_ruff_action

ci: Added using ruff action for CI linting ([`5d7137b`](https://github.com/tattle-made/feluda/commit/5d7137bb29e71a09d30ece4fc9e535bd9c8dd872))


## v0.5.1 (2024-03-23)

### Chore

* chore: Added security policy ([`2628ddb`](https://github.com/tattle-made/feluda/commit/2628ddbbaaf05bae7feb794a3c4c9fed53b650b7))

### Ci

* ci: Fix bandit to run from single workflow
- Added bandit.yml to run on PR
- Disabled bandit from pr-security.yml ([`e441f2e`](https://github.com/tattle-made/feluda/commit/e441f2e14291451d70b61ca955dae71ecc3646cd))

* ci: Added ci test for media file hash operator ([`e5f6414`](https://github.com/tattle-made/feluda/commit/e5f64141f3c594f04e0d6f5701a3ae5d9c98bfff))

### Fix

* fix: Added pinned pip package
- Added base requirements.in with pip
- Created base requirements.txt with pip pinned by hash
- Recreated requirements.txt with --allow-unsafe to get correct setuptools
- Updated feluda core dockerfile to install pip using base requirements
- Updated ci test dockerfile to install pip using base requirements
- Updated all benchmark dockerfiles to install pip using base requirements
- Updated all worker dockerfiles to install pip using base requirements
- Updated readme pip install and pip-compile commands ([`810a45e`](https://github.com/tattle-made/feluda/commit/810a45eae4b681799173286b683e64b2d387e38f))

### Unknown

* Merge pull request #239 from tattle-made/hotfix

Hotfix ([`3113756`](https://github.com/tattle-made/feluda/commit/31137560f3099895918e4e27d35d9537a8344074))

* Merge pull request #238 from duggalsu/add_base_requirements

Add base requirements ([`0391f2a`](https://github.com/tattle-made/feluda/commit/0391f2a5cbc6ab05d663332e3c35179581398479))

* Merge pull request #237 from tattle-made/hotfix

Hotfix ([`83e2efd`](https://github.com/tattle-made/feluda/commit/83e2efd7d643ccd89c1be9c9131e2428dae7aa5e))

* Merge pull request #236 from duggalsu/fix_bandit_codeql_warning

Fix bandit codeql warning ([`a7c05bb`](https://github.com/tattle-made/feluda/commit/a7c05bba72bbff11c5aac44f7e93959f09a3e557))

* - Test inverted ternary operator ([`fe03cb5`](https://github.com/tattle-made/feluda/commit/fe03cb5059c53771f7d8f32098f678795be9037c))

* - Modify env settings ([`2d48897`](https://github.com/tattle-made/feluda/commit/2d488971013c8cdccc0fd84f320ad012571a7f9e))

* - Test switch conditional values ([`7f1315a`](https://github.com/tattle-made/feluda/commit/7f1315a3318f71cc4d915f974369a97c2e392f83))

* - Set conditional falsy and truthy values ([`f85d164`](https://github.com/tattle-made/feluda/commit/f85d164d8237b8a01d2f3ffa72c82c383f5268cd))

* - Fix env var boolean setting ([`68923a6`](https://github.com/tattle-made/feluda/commit/68923a683dffaeecb2697e51f7d5be16a7e51141))

* - Added conditional exit_zero for bandit ([`764b8bb`](https://github.com/tattle-made/feluda/commit/764b8bbf79a9caa3f3445ad9d1981309739704ea))

* Merge pull request #235 from tattle-made/hotfix

Hotfix ([`650a379`](https://github.com/tattle-made/feluda/commit/650a379bbc6ecc92ae4cc5a0e397d17e04a69578))

* Merge pull request #234 from duggalsu/add_ci_test_media_file_hash

Add ci test media file hash ([`88f1d30`](https://github.com/tattle-made/feluda/commit/88f1d3062ef3ada6ecb767cb389c50db9ebfebf5))

* Merge pull request #233 from tattle-made/hotfix

Hotfix ([`13829a6`](https://github.com/tattle-made/feluda/commit/13829a6d4b72dbb49450572d5d827e0c2b88a952))

* Merge pull request #232 from duggalsu/add_security_policy

Add security policy ([`f0f6d70`](https://github.com/tattle-made/feluda/commit/f0f6d701dc3117c16c0e542c0201784c6ae8d7f9))


## v0.5.0 (2024-03-21)

### Chore

* chore: adding context manager to audio operator ([`38f610f`](https://github.com/tattle-made/feluda/commit/38f610fa6101fcdcd80b02d43e61dec514685e1a))

* chore: updating table name ([`c015d30`](https://github.com/tattle-made/feluda/commit/c015d30b9dad79617195b1cab31a4b6491490933))

### Ci

* ci: Added PR checks to run on main branch ([`efc63e7`](https://github.com/tattle-made/feluda/commit/efc63e716bfd224bad7cc07864ab0db999bd24cb))

### Feature

* feat: Added audio CRC write to postgres
- Modified video worker column value ([`17ca1a7`](https://github.com/tattle-made/feluda/commit/17ca1a72b8b47ba9203a9ac7f107e40d5b4d248d))

* feat: Add video CRC to postgres
- Created trigger function for updating timestamp
- Modified create table function with conditional for table
- Added create table for storing CRC
- Added function to create trigger for table
- Modified store and update functions to store worker_column
- Added postgres init and call to storing video CRC
- Pinned images in docker compose ([`f11e1c8`](https://github.com/tattle-made/feluda/commit/f11e1c844512e138e7420a5469416f9707cc2b3e))

* feat: hash worker can add data to postgresql ([`eae1993`](https://github.com/tattle-made/feluda/commit/eae1993db5f043b1c8e04b4fb7fcec4d67191114))

* feat: Added creation of CRC for video and audio vec for media matching ([`ca52993`](https://github.com/tattle-made/feluda/commit/ca529937c13f6b998541d6e0363d179991426232))

* feat: Add calculating video vec CRC for media matching ([`9d57125`](https://github.com/tattle-made/feluda/commit/9d571257f8bb41a495160a62847ca46db4ab838c))

### Fix

* fix(security): SQL issues
- Replaced all dynamic SQL with prepared statements
- Removed all f-strings
- Added str conversion to hash function on db store as failsafe ([`8e86b2a`](https://github.com/tattle-made/feluda/commit/8e86b2a0937a3092ba49c8357a5ad7753daa3cc3))

* fix(security): SQL issues

# Conflicts:
#	src/core/store/postgresql.py ([`3a5f003`](https://github.com/tattle-made/feluda/commit/3a5f003cafe0e1342eb352aea2e59a514b9bc475))

* fix: store and update postgres functions to support hash worker ([`1511228`](https://github.com/tattle-made/feluda/commit/151122862a4cfe1adbaf9dbdd7999f3c5319e5e2))

* fix: postgres store and update func in hash worker ([`f7cb056`](https://github.com/tattle-made/feluda/commit/f7cb056fc9cd7a201ebb8d73726857dc5438ed51))

* fix: Update urllib3 package and fix feluda core dockerfile
- Updated urllib3 manually for botocore compatibility
- Updated groupadd, useradd and mkdir commands to handle failure
- Added setting python user to debug image
- Added venv volume to feluda api in docker compose file
- Added build args for feluda indexer and reporter
- Added volumes in docker compose file ([`317c2a0`](https://github.com/tattle-made/feluda/commit/317c2a09a7bfa0daebff97b78ff5d35a05c06af3))

### Refactor

* refactor: commenting init func ([`bbdffbe`](https://github.com/tattle-made/feluda/commit/bbdffbece59cd5fb737f48df6299235f4c0aa542))

### Unknown

* Merge pull request #230 from tattle-made/development

merge dev to main ([`ed75278`](https://github.com/tattle-made/feluda/commit/ed752788090d1b1c7fdfa84e6389116bd68985ac))

* Merge pull request #229 from duggalsu/test_sql

Fix SQL queries ([`81a99ed`](https://github.com/tattle-made/feluda/commit/81a99eda41303fb1f7138a5453640d3d2652ed8f))

* Merge pull request #228 from aatmanvaidya/hash-worker-update

fix: postgres store and update func in hash worker ([`27f6715`](https://github.com/tattle-made/feluda/commit/27f671523fa2eb9643308d884b8244be9bbac743))

* Merge pull request #227 from aatmanvaidya/audio-delete

chore: adding context manager to audio operator ([`bd6202f`](https://github.com/tattle-made/feluda/commit/bd6202ff12b06612f529285f44a1821c2b1f9678))

* Merge pull request #226 from duggalsu/add_crc_postgres_audio

feat: Added audio CRC write to postgres ([`ddc008a`](https://github.com/tattle-made/feluda/commit/ddc008a4beffcb55d71080670968b0965c6d5692))

* Merge pull request #225 from duggalsu/add_crc_postgres

feat: Add video CRC to postgres ([`6d173bb`](https://github.com/tattle-made/feluda/commit/6d173bba4a729a172697b2059737d34029ffbb28))

* Merge pull request #224 from tattle-made/hotfix

Hotfix ([`34f3ed0`](https://github.com/tattle-made/feluda/commit/34f3ed0c6e03ef765cb3c29140f635982ed68c34))

* Merge pull request #223 from duggalsu/add_pr_checks_main

Add pr checks main ([`aceb907`](https://github.com/tattle-made/feluda/commit/aceb9078c991a239d04227214b8519f06635fbbf))

* Merge pull request #222 from duggalsu/update_urllib3_audio_video_requirements

fix: Update urllib3 package and fix feluda core dockerfile ([`e5e5f4e`](https://github.com/tattle-made/feluda/commit/e5e5f4e29e73cc2afc478cc925f00b430b3430d6))

* Merge pull request #221 from aatmanvaidya/postgres-hash

feat: hash worker can add data to postgresql ([`c34a6b3`](https://github.com/tattle-made/feluda/commit/c34a6b39e28d26c01a83f94690101a394009573e))

* Merge pull request #220 from duggalsu/impl_media_crc

Impl media crc ([`f4018b0`](https://github.com/tattle-made/feluda/commit/f4018b01ad62183ae1bde2026aed272da6d5f8a5))


## v0.4.10 (2024-03-18)

### Fix

* fix(ci): Fixed github workflow docker build args format ([`b6a3d14`](https://github.com/tattle-made/feluda/commit/b6a3d14ee6f12b7614fcd2613abc3879a9505f8c))

### Unknown

* Merge pull request #219 from tattle-made/hotfix

Hotfix ([`4b4a3ff`](https://github.com/tattle-made/feluda/commit/4b4a3ffebd2241add79a676d4a196b7ca2e7faa7))

* Merge pull request #218 from duggalsu/fix_docker_build_args_format

Fix docker build args format ([`fe1adfd`](https://github.com/tattle-made/feluda/commit/fe1adfd9593131245889932722ed9f2ece853032))


## v0.4.9 (2024-03-18)

### Fix

* fix(ci): Added docker build args to github workflows ([`496d600`](https://github.com/tattle-made/feluda/commit/496d60029d2ef9cc8b95ed3ca4e88d3d5f511aa0))

### Unknown

* Merge pull request #217 from tattle-made/hotfix

Hotfix ([`c039f63`](https://github.com/tattle-made/feluda/commit/c039f631d7c8f39e7b7a123fc17519f5103a103d))

* Merge pull request #216 from duggalsu/fix_docker_build_args

Fix docker build args ([`ef9c159`](https://github.com/tattle-made/feluda/commit/ef9c1596b79595bbfab65b5b0b71dc3fe520dc09))


## v0.4.8 (2024-03-18)

### Fix

* fix: Fixed volume sync and non-root user permission issues ([`5fd4258`](https://github.com/tattle-made/feluda/commit/5fd42588ecf7f8edaae528fcdb0e61e701d64ae8))

### Unknown

* Merge pull request #215 from tattle-made/hotfix

Hotfix ([`20ed58a`](https://github.com/tattle-made/feluda/commit/20ed58aa398fad0e6acb58e07e6529fd5c15c895))

* Merge pull request #214 from duggalsu/fix_volume_sync

Fix volume sync ([`772d71d`](https://github.com/tattle-made/feluda/commit/772d71da92180f630dea452acb7a4d114ff4c6f1))

* - Added UID and GID args to ci-sut docker compose ([`3bdb16a`](https://github.com/tattle-made/feluda/commit/3bdb16ad7dbab3936ceccf697c86e6d53a6f8d7d))


## v0.4.7 (2024-03-18)

### Ci

* ci: remove intermediate cache deletion step ([`ade1e67`](https://github.com/tattle-made/feluda/commit/ade1e6795a886e497c7910f7839358389db0398b))

* ci: updated dockerfile base image platform ([`d0542bf`](https://github.com/tattle-made/feluda/commit/d0542bf63a0469f83ff053e9e7621dfe4f7bf454))

* ci: Add github cache action for local key-based caching ([`7b8ed07`](https://github.com/tattle-made/feluda/commit/7b8ed07566cfc6430ab8678b37df20ffca81c291))

* ci: Added dependabot config ([`8a57943`](https://github.com/tattle-made/feluda/commit/8a57943ed43b2feb7b4a7b19d1bdd7c20ac4e68b))

### Fix

* fix: Remove github caching and modify base image to use TARGETPLATFORM ([`0dfb172`](https://github.com/tattle-made/feluda/commit/0dfb17245c54d7efb81da38d72fb66daa09e70b9))

### Unknown

* Merge pull request #213 from tattle-made/hotfix

Hotfix ([`4541139`](https://github.com/tattle-made/feluda/commit/4541139173016b62bcb254d932ee1396667dea10))

* Merge pull request #212 from duggalsu/remove_github_caching

Remove GitHub caching ([`c490cea`](https://github.com/tattle-made/feluda/commit/c490cea40a5611249cff6cef99d97096c2132e08))

* Merge pull request #211 from tattle-made/hotfix

Hotfix ([`cdb081a`](https://github.com/tattle-made/feluda/commit/cdb081a603b326953259137757513ced996cf4c5))

* Merge pull request #210 from duggalsu/rm_intermediate_cache_del

Rm intermediate cache del ([`caae5a8`](https://github.com/tattle-made/feluda/commit/caae5a8202ab6b4326d8b663689cbf0e3adb980c))

* Merge pull request #209 from tattle-made/hotfix

Hotfix ([`decd119`](https://github.com/tattle-made/feluda/commit/decd119bd39781281a7f47151280b34dd4f90763))

* Merge pull request #208 from duggalsu/modify_base_img_platform

Modify base img platform ([`c48efa4`](https://github.com/tattle-made/feluda/commit/c48efa4af4aae2eeeb461eb4d5049e17bccb8b82))

* Merge pull request #201 from tattle-made/hotfix

Hotfix ([`d91149a`](https://github.com/tattle-made/feluda/commit/d91149ab2602dcce0096451824726fe0cb52c943))

* Merge pull request #200 from duggalsu/fix_github_caching

Fix GitHub caching ([`389f021`](https://github.com/tattle-made/feluda/commit/389f0213b493e5b4acd498cdd5881f925b2bd9d3))

* Merge pull request #190 from tattle-made/hotfix

Hotfix ([`5d13eea`](https://github.com/tattle-made/feluda/commit/5d13eeaf50635f5faadbb7aa2819410d5b6a59b1))

* Merge pull request #189 from duggalsu/add_dependabot_yml

Add dependabot yml ([`74945f2`](https://github.com/tattle-made/feluda/commit/74945f2643f99b70f598538e3cb52460bdcfa420))


## v0.4.6 (2024-03-17)

### Ci

* ci: removed require hashes to allow no-deps to work ([`e634622`](https://github.com/tattle-made/feluda/commit/e6346228df9eace2204e54915439ff9ddf838101))

* ci: added no deps and require hashes for pip audit ([`e5f110c`](https://github.com/tattle-made/feluda/commit/e5f110ceb5184e4a0c2017a950d351fefb9f9946))

### Fix

* fix: Security enhancements and performance optimizations
- security: Removed exposed port in all workers
- security: Pinned docker platform in all dockerfile images
- security: Pinned docker images digest in all dockerfile images
- security: Pinned python packages by hash digest in all dockerfile images
- perf: Optimized workers and test image for smaller size and build times
- perf: Enabled github docker cache for all workflows
- docs: Updated readme with generate hash instructions for requirements ([`7b181af`](https://github.com/tattle-made/feluda/commit/7b181af09738467ee8e37f24bb664c858cccb6c4))

### Unknown

* Merge pull request #188 from tattle-made/hotfix

Hotfix ([`f92ef82`](https://github.com/tattle-made/feluda/commit/f92ef820710bcf5f4dfe2e874d58128e0df0dea3))

* Merge pull request #187 from duggalsu/opt_vid_worker

Opt vid worker ([`217d60d`](https://github.com/tattle-made/feluda/commit/217d60d744cfd556c1dab8e55e801dffc4848fd7))

* - setup python version ([`2d1863c`](https://github.com/tattle-made/feluda/commit/2d1863c3be284b71d99354b82ebc1c1061c5422f))


## v0.4.5 (2024-03-15)

### Ci

* ci: removed explict checkout in docker build ([`2068476`](https://github.com/tattle-made/feluda/commit/206847606128fd7de54d59274c64d4592a162e3f))

* ci: fix context in test workflow ([`201c900`](https://github.com/tattle-made/feluda/commit/201c900b7d67bc55df7bc3de4b9d9351f692ea3d))

* ci: Fix issues with docker push vidvec benchmark test workflow ([`1d4a31e`](https://github.com/tattle-made/feluda/commit/1d4a31e31d9a7f80aee71ee1df93c4a28b0448c9))

### Fix

* fix: Fix workflows ([`c356dc9`](https://github.com/tattle-made/feluda/commit/c356dc9cfb69211686fbcb3a1fbb076acc01f6f3))

### Unknown

* Merge pull request #186 from tattle-made/hotfix

Hotfix ([`2c19559`](https://github.com/tattle-made/feluda/commit/2c195594ce9984dd36d52c1b0210807f1bde2329))

* Merge pull request #185 from duggalsu/fix_docker_workflow

Fix docker workflow ([`acc4000`](https://github.com/tattle-made/feluda/commit/acc4000c3939c1f3c9829f9eb5fdc863086c1942))

* Merge pull request #184 from tattle-made/hotfix

Hotfix ([`3d6c84f`](https://github.com/tattle-made/feluda/commit/3d6c84fbe7d53ba99ed5b6dac071e918bda9afa5))

* Merge pull request #183 from duggalsu/fix_vidvec_benchmark_test_workflow_2

Fix vidvec benchmark test workflow 2 ([`7d5cc01`](https://github.com/tattle-made/feluda/commit/7d5cc0168735453dded3138f26fc70c6e037df17))

* Merge pull request #182 from tattle-made/hotfix

Hotfix ([`f6d87f8`](https://github.com/tattle-made/feluda/commit/f6d87f8c2ff893d5a8ff41b3ca6cbfd87b1d1fff))

* Merge pull request #181 from duggalsu/fix_vidvec_benchmark_test_workflow

Fix vidvec benchmark test workflow ([`6f2a32a`](https://github.com/tattle-made/feluda/commit/6f2a32a3ed2a663c180604cd70259ad90dc7baa2))

* Merge pull request #180 from tattle-made/hotfix

Hotfix ([`0b30a78`](https://github.com/tattle-made/feluda/commit/0b30a78e503a5533bf8c6d38eaa08165d6ef26af))

* Merge pull request #179 from tattle-made/scorecard_workflow

Scorecard workflow ([`d1f468d`](https://github.com/tattle-made/feluda/commit/d1f468d545193a0a077f876faf474b6e7e3ba2b7))

* Create scorecard.yml ([`7bf1e20`](https://github.com/tattle-made/feluda/commit/7bf1e2015672db2f82ef47e05b4a8ee4d739f3da))


## v0.4.4 (2024-03-14)

### Chore

* chore: removed global import ([`d02366c`](https://github.com/tattle-made/feluda/commit/d02366c90399c39cd691f7d78104ff750bc553a7))

### Fix

* fix: tempfile path for make from file in memory function ([`831a700`](https://github.com/tattle-made/feluda/commit/831a70005eaab0e5b9a67b4db215e8c8b633f158))

* fix: tempfile impl ([`2f9cc07`](https://github.com/tattle-made/feluda/commit/2f9cc077e29915e9422e01c723e0a48dcc70f8d3))

* fix: Removed use of tempfile downloads ([`eb97f09`](https://github.com/tattle-made/feluda/commit/eb97f09ba5396457c82a9f97db25cf2aa6cf6755))

* fix: Created tempfile safely ([`badc043`](https://github.com/tattle-made/feluda/commit/badc0436c55387b1b540096cc6185c91d9563f7d))

### Unknown

* Merge pull request #178 from tattle-made/hotfix

Hotfix ([`a85423a`](https://github.com/tattle-made/feluda/commit/a85423a44e26ef3fb56700853f9d5a517712c29f))

* Merge pull request #164 from duggalsu/fix_tempfile_issues

Fix tempfile issues ([`c846df5`](https://github.com/tattle-made/feluda/commit/c846df5f57ef2bfb4b4f6bcbac7551f504c759df))

* Merge remote-tracking branch &#39;refs/remotes/origin/fix_tempfile_issues&#39; into fix_tempfile_issues

# Conflicts:
#	src/core/models/media_factory.py ([`36ec52b`](https://github.com/tattle-made/feluda/commit/36ec52b111b788ad424fb0f27562e0ffafa6b650))

* Fix tempfile issues
- Optimized dockerfile
- Modified tempfile tests ([`d082d93`](https://github.com/tattle-made/feluda/commit/d082d937f39240f66a19424a5081769410e21852))

* - Fixed video and audio file return path ([`bc43d19`](https://github.com/tattle-made/feluda/commit/bc43d1986a08d8314f8abf9d3976f49f5b9ed669))


## v0.4.3 (2024-03-14)

### Fix

* fix: flask issues
- Added config vars to env template
- Disabled flask production docker image
- Enabled flask dev server and debugpy to run on localhost
- Added debug cmd flag as recommended approach
- Modified flask app run to load host and debug values from env ([`cfc0601`](https://github.com/tattle-made/feluda/commit/cfc0601bec2c7e29044c2bc48d53cf077e50e6da))

### Unknown

* Merge pull request #177 from tattle-made/hotfix

Hotfix ([`f2a2b3d`](https://github.com/tattle-made/feluda/commit/f2a2b3d770063795cea0615f17c9477781aaa8b5))

* Merge pull request #176 from duggalsu/fix_flask_issues

Fix flask issues ([`c68596f`](https://github.com/tattle-made/feluda/commit/c68596fd380ab7df68b4c9654f9fc2e3197b79f1))


## v0.4.2 (2024-03-13)

### Fix

* fix: wget issues ([`ff70726`](https://github.com/tattle-made/feluda/commit/ff707269a2a02325de8bb7d38ff2324a50d763fc))

### Unknown

* Merge pull request #175 from tattle-made/hotfix

Hotfix ([`fc508fa`](https://github.com/tattle-made/feluda/commit/fc508fa4f0d39695a55c31f107379e2fd64daf43))

* Merge pull request #174 from duggalsu/fix_wget_issues

Fix wget issues ([`6b98b8f`](https://github.com/tattle-made/feluda/commit/6b98b8f08d361f3d7f99071e9fc9c40685eb14f9))


## v0.4.1 (2024-03-13)

### Fix

* fix: Renamed hash worker graviton file
ci: Added publishing media hash worker docker images
ci: Added release hash worker dockerfiles ([`33fb2d8`](https://github.com/tattle-made/feluda/commit/33fb2d84049576912c2d6c1b9b4691fa24d978e2))

### Unknown

* Merge pull request #173 from tattle-made/hotfix

Hotfix ([`ec7b922`](https://github.com/tattle-made/feluda/commit/ec7b922fd83628816408196ea5d675c2b5fb7a93))

* Merge pull request #172 from duggalsu/add_hash_worker_workflow

Add hash worker workflow ([`b58c11f`](https://github.com/tattle-made/feluda/commit/b58c11f98b240dbe2d5d28e787002f8155901cdc))


## v0.4.0 (2024-03-13)

### Ci

* ci: updating hash worker github workflow ([`73e5634`](https://github.com/tattle-made/feluda/commit/73e5634d462064f3fa4d38aec72ed126cc17aeea))

### Fix

* fix: subprocess call issue ([`058cee5`](https://github.com/tattle-made/feluda/commit/058cee5eeaef56c9704b4745f6cd9298b16cca35))

### Unknown

* Merge pull request #165 from tattle-made/development

merge dev to main ([`55204f9`](https://github.com/tattle-made/feluda/commit/55204f9c60a466de06d8b102b66d5d85b48b1c91))

* Merge pull request #166 from aatmanvaidya/temp-dev-2

resolving merge conflicts ([`1dea270`](https://github.com/tattle-made/feluda/commit/1dea2707bbf211fb8b91c3335b71e1675d51e0f1))

* Merge remote-tracking branch &#39;upstream/main&#39; into temp-dev-2 ([`3c28a9f`](https://github.com/tattle-made/feluda/commit/3c28a9f310413ce67264f069d1ab067f206ef014))

* Merge pull request #171 from duggalsu/fix_subprocess_call

Fix subprocess call ([`acf4974`](https://github.com/tattle-made/feluda/commit/acf4974c5374e1fe2f59cc2d33bb6c77c6b2c199))


## v0.3.4 (2024-03-13)

### Chore

* chore: fixing module imports ([`4097614`](https://github.com/tattle-made/feluda/commit/4097614dd86b9edef88855771383faf2de6f1365))

* chore: resolving merge conflicts ([`5e3da48`](https://github.com/tattle-made/feluda/commit/5e3da48f102cf1858078748444e1eb7bb40768a9))

### Ci

* ci: fixing hash worker dockerfiles ([`46173da`](https://github.com/tattle-made/feluda/commit/46173da54423a70a7f295862f7106cf98aceb6de))

### Fix

* fix: Fixed yaml load ([`0582882`](https://github.com/tattle-made/feluda/commit/0582882dec8322ab42bd2f7dc69206677858b633))

* fix: Fixed assert issues ([`33f5fd2`](https://github.com/tattle-made/feluda/commit/33f5fd25a137c9176542be50e5fef39a730ebab0))

* fix: linting issues ([`39d90be`](https://github.com/tattle-made/feluda/commit/39d90beb4caf35d93b4364360796d1932f177510))

* fix: Removed secrets ([`11f4186`](https://github.com/tattle-made/feluda/commit/11f4186526ad0437ca5d62fc78216be5fd90f3fa))

* fix: Created tempfile safely ([`fc0d3a2`](https://github.com/tattle-made/feluda/commit/fc0d3a2b8e70aa17ebae6f76da9099699b911afb))

* fix: hash operator and worker ([`64d0797`](https://github.com/tattle-made/feluda/commit/64d0797b98ffb90ce5569f587b6403b9373893cf))

### Unknown

* Merge pull request #170 from tattle-made/hotfix

Hotfix ([`8f4e730`](https://github.com/tattle-made/feluda/commit/8f4e730d757094a0396fb71fb5139bd62c171280))

* Merge pull request #169 from duggalsu/fix_yaml_load

fix: Fixed yaml load ([`ab3851f`](https://github.com/tattle-made/feluda/commit/ab3851f41ce1e7820f1e849e24724edda6c44906))

* Merge pull request #168 from duggalsu/fix_assert_issues

fix: Fixed assert issues ([`1290ef9`](https://github.com/tattle-made/feluda/commit/1290ef9e4d23749dc356da5ff2b2aa650fbfe7ca))

* Merge pull request #167 from duggalsu/fix_secrets

Fix secrets ([`3670bc9`](https://github.com/tattle-made/feluda/commit/3670bc973ae4a0fc699780fa8a3a91b1efcdd4b0))

* - Fixed video and audio file return path ([`a251873`](https://github.com/tattle-made/feluda/commit/a2518731af3474881b62505fa10e77267ab163f5))

* Merge pull request #163 from aatmanvaidya/hash-op

fix: hash operator and worker ([`d51aeb3`](https://github.com/tattle-made/feluda/commit/d51aeb3fbe23bf73235f754534f17667679bd660))


## v0.3.3 (2024-03-12)

### Chore

* chore: updated numpy version ([`a299171`](https://github.com/tattle-made/feluda/commit/a299171f166605d6e344876a573ed809f75a660a))

### Ci

* ci: Add bandit cron workflow to trigger on push to main for resolved issues ([`90864bd`](https://github.com/tattle-made/feluda/commit/90864bd87f46682e80586052b2f3a6667f940a7c))

* ci: Updated cron time to test trigger ([`170c313`](https://github.com/tattle-made/feluda/commit/170c313467210a10561b3564e26ccb48977a4844))

* ci: Enabled github token and modified cron UTC time ([`89c773f`](https://github.com/tattle-made/feluda/commit/89c773f7f5478a4a7a9e06d647575147932975df))

* ci: Updated path settings ([`b02ed5b`](https://github.com/tattle-made/feluda/commit/b02ed5bd859d03aa22328a0545a1f354f672822d))

* ci: Fix bandit cron workflow ([`faf897f`](https://github.com/tattle-made/feluda/commit/faf897f6f43f9e1524db15b20a3021c49f141cc5))

* ci: Disabled bandit level ([`4802bea`](https://github.com/tattle-made/feluda/commit/4802bea43852c1997a766ecf237d909d02639629))

* ci: Added bandit SAST scanning ([`5ecd5da`](https://github.com/tattle-made/feluda/commit/5ecd5da966697adccf1e9281039f58e4e251b7db))

* ci: fixed scanners option ([`ae1ceb4`](https://github.com/tattle-made/feluda/commit/ae1ceb4f4fa2e399ec0ba2137bc9cb24e5925189))

* ci: Added exit code with limit sarif severities and always upload results ([`b105ac5`](https://github.com/tattle-made/feluda/commit/b105ac54971bb0e55d2d54b2a82eb1e41d119cd9))

* ci: Updated codeql-action version ([`03e48ea`](https://github.com/tattle-made/feluda/commit/03e48eadcc3aca6d2c302817c641ac2f0e7d5fe8))

* ci: Removed failure condition for trivy scan to allow sarif upload ([`7b17253`](https://github.com/tattle-made/feluda/commit/7b1725375901b441ff7ed506d6c76ce2fdbd7ae3))

* ci: Added githbu codeql sarif upload permissions ([`1bcd94b`](https://github.com/tattle-made/feluda/commit/1bcd94b8652610cd59597e3bb372d3a3747ec54f))

* ci: Enabled trivy result upload to github codeql ([`e9afff0`](https://github.com/tattle-made/feluda/commit/e9afff0b53bbb35e284bfd4ca279e0021910e7a3))

* ci: separate pip audit ([`e93e002`](https://github.com/tattle-made/feluda/commit/e93e002a12ff341f4a20375d0bd2fa85097a1aee))

* ci: add pip audit security workflow ([`b7a4db2`](https://github.com/tattle-made/feluda/commit/b7a4db2cea64244af9b3889d9f1ea4fa70b1636a))

### Fix

* fix: (security) Added timeout to requests ([`f5c0645`](https://github.com/tattle-made/feluda/commit/f5c064540ebef3c1577a8706f4f6d28a0dfc5549))

### Unknown

* Merge pull request #162 from tattle-made/hotfix

Hotfix ([`9c7d06b`](https://github.com/tattle-made/feluda/commit/9c7d06b2ec993fda29dcdab04e94c58213912240))

* Merge pull request #161 from duggalsu/add_requests_timeout

Add requests timeout ([`805e426`](https://github.com/tattle-made/feluda/commit/805e426b9d32d3d9ad4c086a56030a93d922a9ff))

* Merge pull request #160 from tattle-made/hotfix

Hotfix ([`76d900e`](https://github.com/tattle-made/feluda/commit/76d900e554860f6b8d5a7ad9e8c0580a23328e4f))

* Merge pull request #159 from duggalsu/add_on_push_bandit_cron_workflow

Add on push bandit cron workflow ([`bb97334`](https://github.com/tattle-made/feluda/commit/bb97334b4ae08074f3f9ad275cd1ce7380694689))

* Merge pull request #158 from tattle-made/hotfix

Hotfix ([`7b29e51`](https://github.com/tattle-made/feluda/commit/7b29e5171286c2c8aee6240c0ed7098acfe437f5))

* Merge pull request #157 from duggalsu/test_bandit_cron_workflow_2

Test bandit cron workflow 2 ([`5ef5baf`](https://github.com/tattle-made/feluda/commit/5ef5baf52174bd7cd88d2626abf14347540294c7))

* Merge pull request #156 from tattle-made/hotfix

Hotfix ([`dc387bc`](https://github.com/tattle-made/feluda/commit/dc387bce7034fc4bad0f8f3d96d5ff9ba235531b))

* Merge pull request #155 from duggalsu/test_bandit_cron_workflow

Test bandit cron workflow ([`bba6af8`](https://github.com/tattle-made/feluda/commit/bba6af876fddf1bb1090adbb11798667544af12c))

* Merge pull request #154 from tattle-made/hotfix

Hotfix ([`9fca369`](https://github.com/tattle-made/feluda/commit/9fca369f6896259a104b42cd2f4eb6ed1bee9694))

* Merge pull request #153 from duggalsu/fix_bandit_cron_workflow

Fix bandit cron workflow ([`d4f7e01`](https://github.com/tattle-made/feluda/commit/d4f7e01b078dcae482ae30144fc0985cf9a35d9d))

* Merge pull request #152 from tattle-made/hotfix

Hotfix ([`0605f12`](https://github.com/tattle-made/feluda/commit/0605f12043c25892d162e8038c8ab89522bb989c))

* Merge pull request #151 from tattle-made/bandit_cron_job

Bandit cron job ([`453093d`](https://github.com/tattle-made/feluda/commit/453093d34f70821b5e931d9190e18435f4e35df1))

* Create bandit.yml ([`f9f5e2b`](https://github.com/tattle-made/feluda/commit/f9f5e2b97de86557e4ebe8916d0c47e56f35b7cd))

* Merge pull request #150 from tattle-made/hotfix

Hotfix ([`5355a37`](https://github.com/tattle-made/feluda/commit/5355a374ba3d4c1e549d47f09de024087efc6534))

* Merge pull request #149 from duggalsu/add_ci_bandit

Add ci bandit ([`c899ab4`](https://github.com/tattle-made/feluda/commit/c899ab42dd9b6efc0878126ef6c1f6c0be15d2b3))

* Merge pull request #148 from tattle-made/hotfix

Hotfix ([`1001e92`](https://github.com/tattle-made/feluda/commit/1001e92ec4157c8af7778fe8bc480691e7669386))

* Merge pull request #147 from duggalsu/add_ci_trivy

Add ci trivy ([`0f7e440`](https://github.com/tattle-made/feluda/commit/0f7e440ca3fd0ff1dafb748ef6e3d58a766f5360))

* ci (security): Added IaC scan with Trivy ([`ac487f9`](https://github.com/tattle-made/feluda/commit/ac487f93c3a8e35f835f39ab1e2bb257978d16a1))

* fix (security): Renamed graviton dockerfiles for detection by trivy ([`bc2b01c`](https://github.com/tattle-made/feluda/commit/bc2b01c1e24520abb2e0289b7479627f7997bcd3))

* fix (security): Harden dockerfiles
- Added unprivileged python user
- Created venv for all pip install
- Added chown for all files and dirs
- Added --no-install-recommends to apt-get install cmd
- Fixed feluda core server.py import issue ([`a760d2e`](https://github.com/tattle-made/feluda/commit/a760d2ee4626b9094607470de6f3bf2ebcd3cb5e))

* Merge pull request #146 from tattle-made/hotfix

Hotfix ([`adf12d0`](https://github.com/tattle-made/feluda/commit/adf12d0130571669a805e7a221b9b2ab1e2ebcaa))

* Merge pull request #145 from duggalsu/add_ci_pip_audit

Add ci pip audit ([`40f3ff6`](https://github.com/tattle-made/feluda/commit/40f3ff6f0833ba0c9402818ca933333803ae7dcd))


## v0.3.2 (2024-03-07)

### Chore

* chore: fixing docker-compose.yml ([`3fe5de6`](https://github.com/tattle-made/feluda/commit/3fe5de666deacb12c1ae755e860dec83a1c7e35a))

### Ci

* ci: github action to push md5hash worker to staging ([`b5df260`](https://github.com/tattle-made/feluda/commit/b5df26034280af5178f246c46308c5bd3856631d))

* ci: add security checks on PR ([`ca7de73`](https://github.com/tattle-made/feluda/commit/ca7de732d8ed98cdf2d650e1bc0c5f30012f4803))

### Feature

* feat: worker for md5hash operator ([`008cc8d`](https://github.com/tattle-made/feluda/commit/008cc8d52dbfa594db5b861f5374298b4b5a44b9))

### Fix

* fix: linter formatting ([`4758315`](https://github.com/tattle-made/feluda/commit/4758315113d9b9de5c62600936e34c8ecc54f556))

* fix: linter issues ([`11f3683`](https://github.com/tattle-made/feluda/commit/11f3683fdaef8abf46d635343213444e7cf3ba4b))

### Unknown

* Merge pull request #144 from tattle-made/hotfix

Hotfix ([`dc64745`](https://github.com/tattle-made/feluda/commit/dc64745059fc7185e73b99ec530865054edd0df2))

* Merge pull request #143 from aatmanvaidya/md5-ci

ci: github action to push md5hash worker to staging ([`c896d29`](https://github.com/tattle-made/feluda/commit/c896d29bd76f3cd7ea39a5b9667ba3f20174e1b2))

* Merge pull request #142 from aatmanvaidya/md5-hash-worker

feat: worker for md5hash operator ([`da40ef9`](https://github.com/tattle-made/feluda/commit/da40ef96dfa88cb09f03f110ebcd7e6c7b59a62e))

* Merge pull request #135 from duggalsu/test_official_docker_push_action

Test official docker push action ([`1dbe184`](https://github.com/tattle-made/feluda/commit/1dbe184665209855c66ad6e8696c9fdccd33a662))

* Merge pull request #141 from duggalsu/fix_linter_issues

Fix linter issues ([`7dd3979`](https://github.com/tattle-made/feluda/commit/7dd397940b7d4fa325fe6552a19c7ed0349ab39d))


## v0.3.1 (2024-03-07)

### Fix

* fix: Dockerfile arm build ([`cce1ebe`](https://github.com/tattle-made/feluda/commit/cce1ebe09f3023c8b1e2e89cf4f867793c2f8c83))

### Unknown

* Merge pull request #140 from tattle-made/hotfix

Hotfix ([`68469b1`](https://github.com/tattle-made/feluda/commit/68469b13186015bd3a411f050e5dc4de676d85d8))

* Merge pull request #139 from aatmanvaidya/fix-dockerfiles

fix: Dockerfile arm build ([`a031c5d`](https://github.com/tattle-made/feluda/commit/a031c5d508ec40ea10b79e4f3235339c3f72236f))


## v0.3.0 (2024-03-07)

### Ci

* ci: Test fix versioning and modify docker images ([`455b77c`](https://github.com/tattle-made/feluda/commit/455b77c0b2692a6eb19b7499db0e18542b1c101f))

* ci: Fix docker yml ([`d0a48f8`](https://github.com/tattle-made/feluda/commit/d0a48f8424de21b928ca0e09c421b87c155cc725))

* ci: Fix yaml issue ([`2f47f19`](https://github.com/tattle-made/feluda/commit/2f47f1985760328c8932c3b5b8c8cbfc31613358))

* ci: Fix yaml issue ([`82bfeb4`](https://github.com/tattle-made/feluda/commit/82bfeb4e545ed15b2f2795bdcac8fcb9dc7c2870))

* ci: Test fix versioning and modify docker images ([`ae54bcd`](https://github.com/tattle-made/feluda/commit/ae54bcdbfdb3d0b3fde6e7573d7eb9b0ca57e2bd))

* ci: Add worker docker push ([`97abfb0`](https://github.com/tattle-made/feluda/commit/97abfb06817e915fc5886fcb874cb09010dcc0ec))

* ci: Fix docker yml ([`93f1e51`](https://github.com/tattle-made/feluda/commit/93f1e51ce074ef7998b9719a6003e24416367a13))

* ci: Fix yaml issue ([`a320c49`](https://github.com/tattle-made/feluda/commit/a320c493fff2ab4fdddd12bb0b68e0c728055d51))

* ci: Fix yaml issue ([`148fd8d`](https://github.com/tattle-made/feluda/commit/148fd8d5eba83d023abd8869ec4c7408bf579955))

### Feature

* feat: workers to search audio and video files ([`2301c98`](https://github.com/tattle-made/feluda/commit/2301c984b06319adafdd9fda7ea9aa9592ff5991))

* feat: workers to search audio and video files ([`cd94344`](https://github.com/tattle-made/feluda/commit/cd943449b2d94a92e5c62ce2244a73db3955eea0))

* feat: workers can report to queue ([`3c59999`](https://github.com/tattle-made/feluda/commit/3c59999681a4dc9eabde7fc467b76bec25cb4c69))

### Style

* style: fixing logger ([`dc86b15`](https://github.com/tattle-made/feluda/commit/dc86b154fd0ffbf19f7f5522e835cea1e15d0566))

* style: fixing logger ([`933f6db`](https://github.com/tattle-made/feluda/commit/933f6db71e0a0eb800b98affb3702882f8e3e015))

### Test

* test: official docker build and push workflow ([`4ad6685`](https://github.com/tattle-made/feluda/commit/4ad6685d7a166a50b6f6f4e80c19caff50397929))

### Unknown

* Merge pull request #138 from tattle-made/development

merge development to main ([`df59805`](https://github.com/tattle-made/feluda/commit/df598058143f80f65e546c5af6bfdea825e113a0))

* Merge pull request #136 from aatmanvaidya/worker-search-2

feat: workers to search audio and video files ([`d9c0d1b`](https://github.com/tattle-made/feluda/commit/d9c0d1b518d8201bbf40861f23b0743230655c36))

* Merge branch &#39;worker-search-2&#39; of https://github.com/aatmanvaidya/feluda into worker-search-2 ([`5a55ea7`](https://github.com/tattle-made/feluda/commit/5a55ea789bb5174968fc80c1429cc96025e2e00b))

* Merge pull request #137 from aatmanvaidya/temp-main

rebasing development with main ([`29b36b7`](https://github.com/tattle-made/feluda/commit/29b36b79249e9eeefbcab5f5316cfe1c984479b4))

* ci (fix): Modify pr testing
- Removed integration tests and required components
- Used unittest for unit tests
- Disabled audio from disk test ([`828b1e4`](https://github.com/tattle-made/feluda/commit/828b1e492e4434300e9870ec6bfad11c54b6deb1))

* ci (fix): Increased es java mem limit ([`b4bdee4`](https://github.com/tattle-made/feluda/commit/b4bdee409885eff3ff3ad9954f5eb306bf3b6730))

* ci (fix): version output ([`16add46`](https://github.com/tattle-made/feluda/commit/16add467ccfcc4520efd18f9104ffce5565056b2))

* Merge pull request #134 from tattle-made/hotfix

Hotfix ([`96eab93`](https://github.com/tattle-made/feluda/commit/96eab93ef4f86632c6a4f4862dcfb6d43415cdc6))

* Merge pull request #133 from duggalsu/fix_ci_merge

ci: Test fix versioning and modify docker images ([`09d6941`](https://github.com/tattle-made/feluda/commit/09d69417787a31211bf40680539438dc17078b61))

* Merge branch &#39;hotfix&#39; into fix_ci_merge ([`5775824`](https://github.com/tattle-made/feluda/commit/5775824ab44e5e70934f71eff6f91cf77eb45957))

* Merge pull request #132 from duggalsu/ci_merge_versioning

Ci merge versioning ([`a49c6f5`](https://github.com/tattle-made/feluda/commit/a49c6f5246623f86832d88b71f1b32d3fa6d8ae1))

* Merge pull request #131 from aatmanvaidya/worker-report

feat: workers can report to queue ([`cf801f1`](https://github.com/tattle-made/feluda/commit/cf801f19d56e7f6dd9eecbd21059a346383acddc))

* Merge pull request #130 from tattle-made/hotfix

Hotfix ([`b74f0c7`](https://github.com/tattle-made/feluda/commit/b74f0c7d4e457710e4de01cb46a6ed0d8e87280d))

* Merge pull request #129 from duggalsu/fix_ci_merge_versioning

Fix ci merge versioning ([`4903a49`](https://github.com/tattle-made/feluda/commit/4903a4927b558911b7011e8c4231eaf2881f099e))

* ci (fix): Modify pr testing
- Removed integration tests and required components
- Used unittest for unit tests
- Disabled audio from disk test ([`0a596e0`](https://github.com/tattle-made/feluda/commit/0a596e0c3dcedaf406954390a78253be0f1609ec))

* ci (fix): Increased es java mem limit ([`d39fed4`](https://github.com/tattle-made/feluda/commit/d39fed4d71d5c8acf48d96492d64393c8c93081a))

* ci (fix): version output ([`d3aa1e4`](https://github.com/tattle-made/feluda/commit/d3aa1e4b2bcfff2d97031b761372677a8bfa4a14))


## v0.2.0 (2024-03-05)

### Ci

* ci: allocating more RAM to elasticsearch ([`c0e3f15`](https://github.com/tattle-made/feluda/commit/c0e3f153304ecf3b373347b6d110e0039d30660f))

* ci: Delete workflow
- Deleted merge dev hotfix workflow
- Disabled conditional build on merge main workflow ([`1ba4481`](https://github.com/tattle-made/feluda/commit/1ba4481dee610f5b028a9443fda6781f32c97b9c))

* ci: Fix secrets access
- Removed conditional on merge main workflow
- Removed environment label from merge dev hotfix workflow
- Modified docker secrets name ([`0881176`](https://github.com/tattle-made/feluda/commit/0881176092c63ff6e88df32665b29106efa029a8))

* ci: Fix merge workflows
- Disabled conditional checks on merge main workflow
- Disabled environment setting from merge dev hotfix ([`d094b78`](https://github.com/tattle-made/feluda/commit/d094b78a651bcc445006120654fea1fcf5e716b8))

### Refactor

* refactor: merging development to main ([`5959f74`](https://github.com/tattle-made/feluda/commit/5959f74074e09894cb58906433d3fc1dce673005))

### Test

* test: fixing video es vec ([`bf7dede`](https://github.com/tattle-made/feluda/commit/bf7dedef64b419d88bacb4e5e1a19cb56c597688))

### Unknown

* Merge pull request #128 from tattle-made/development

refactor: merge development to main ([`73cfa5d`](https://github.com/tattle-made/feluda/commit/73cfa5dec7261d1feba08fe2774935ac0eac3bf7))

* Merge pull request #127 from aatmanvaidya/temp-main

refactor: updating dev from main ([`b4dca72`](https://github.com/tattle-made/feluda/commit/b4dca72c491f21a22653621969836bc9601af5f5))

* Merge remote-tracking branch &#39;upstream/development&#39; into temp-main ([`d4415c6`](https://github.com/tattle-made/feluda/commit/d4415c618ea610cf7941f139ff205db7e9f048f0))

* Merge pull request #125 from tattle-made/hotfix

Hotfix ([`06eb74e`](https://github.com/tattle-made/feluda/commit/06eb74ef6ab3457118bc14b0639c07e12f00e4a9))

* Merge pull request #124 from duggalsu/del_merge_dev_hotfix_workflow

ci: Delete workflow ([`0744842`](https://github.com/tattle-made/feluda/commit/07448428baeafe146f9fc4465d7eb42ad2bdd8df))

* Merge remote-tracking branch &#39;upstream/hotfix&#39; into del_merge_dev_hotfix_workflow

# Conflicts:
#	.github/workflows/merge-dev-hotfix.yml ([`3fb216c`](https://github.com/tattle-made/feluda/commit/3fb216c080a7e7487f97157e39129d19fe6dfb0b))

* Merge pull request #122 from duggalsu/fix_ci_merge_secrets_access

ci: Fix secrets access ([`969261c`](https://github.com/tattle-made/feluda/commit/969261c075709a7836a150e2c903629f5530a743))

* Merge pull request #121 from duggalsu/fix_ci_merge_workflow

Fix ci merge workflow ([`0e36a80`](https://github.com/tattle-made/feluda/commit/0e36a805ce53de805d2be537d5f5d235e8988089))

* Merge pull request #120 from aatmanvaidya/main-merge

refactor: merging development to main ([`22bb325`](https://github.com/tattle-made/feluda/commit/22bb325b1b6a5f901bff66ca5d650de40b8d3a0f))


## v0.1.0 (2024-03-04)

### Chore

* chore: fixing spelling in Dockerfile ([`a3e2fbe`](https://github.com/tattle-made/feluda/commit/a3e2fbe374cbd05898d317ead977b32f2044e3c3))

* chore: renaming video worker files ([`10b60b2`](https://github.com/tattle-made/feluda/commit/10b60b2842cf0679faa2a35c8de5b98b2f89211d))

* chore: updating library to local folder location ([`daa91f9`](https://github.com/tattle-made/feluda/commit/daa91f908c51de8fe81abd483903ea6ccd05936c))

* chore: renaming audio cnn model ([`cbdbac9`](https://github.com/tattle-made/feluda/commit/cbdbac9f7b4380d8b5345f43e83a6e63cdafbc28))

* chore: renaming worker files ([`6059355`](https://github.com/tattle-made/feluda/commit/605935594faeebe0a7143bbf198a234a9312f85a))

* chore: renaming operator ([`191abd6`](https://github.com/tattle-made/feluda/commit/191abd692d7f305bb10da0ee525d8164f067f6a2))

* chore: deleting docker-compose-standalone and renaming privacy policy (#89) ([`bf6fb1e`](https://github.com/tattle-made/feluda/commit/bf6fb1e784c57b9614e99c8f23180a25e504b008))

* chore: adding .env-template (#88) ([`c556f8b`](https://github.com/tattle-made/feluda/commit/c556f8bed8dc15dcae9ff9ebd5b24ef49f24b9d2))

* chore: skipping unmaintained tests ([`c48b724`](https://github.com/tattle-made/feluda/commit/c48b72493064a7beebcefc46b6c7384ee04eb32a))

* chore: removing video files ([`bce9759`](https://github.com/tattle-made/feluda/commit/bce975909d4ee7d540fffd368e86b9b45bf59643))

* chore: add DMP issue template ([`63aa375`](https://github.com/tattle-made/feluda/commit/63aa37595c83f1a41eaaef5718dc130855c93b18))

* chore: adding audio file (#73) ([`52d0fd6`](https://github.com/tattle-made/feluda/commit/52d0fd6410cb6155facd0a30ad419dbfec61c4c1))

* chore: not skipping image search test (#57) ([`9f42558`](https://github.com/tattle-made/feluda/commit/9f425587f93e02005554b496c059144c90e19f74))

* chore: revert to commit 8479c38 ([`98a76de`](https://github.com/tattle-made/feluda/commit/98a76de1fa02ee44e2ea2e49760a69202020a207))

* chore: testing ci ([`e909448`](https://github.com/tattle-made/feluda/commit/e909448899945edf9160848955aca74ebc0f7558))

* chore: text vector debugging ([`5097840`](https://github.com/tattle-made/feluda/commit/50978405d331895cf016609668fbfbd4686eb930))

* chore: change batchsize &amp; num_workers to handle memory issue, improve exception logging ([`7cd003e`](https://github.com/tattle-made/feluda/commit/7cd003e3a1e253538f083545ff642dfadb0f7ee2))

### Ci

* ci: Add automated semantic versioning
- Renamed and modified docker push vidvec benchmark yml
- Modified tags and dockerfile name for vidvec worker staging yml
- Added init python file with version number
- Added github workflow on merge on main branch
- Added github workflow on merge on development or hotfix branch ([`972b6a6`](https://github.com/tattle-made/feluda/commit/972b6a68e01210aaea145e8e4284fbe80f68e0f9))

* ci: audiovec worker staging dockerhub tag change ([`a79620d`](https://github.com/tattle-made/feluda/commit/a79620de452a7bfead251759d002ece49a576177))

* ci: audiovec benchmark graviton dockerfile ([`81b02b5`](https://github.com/tattle-made/feluda/commit/81b02b5a759b02e2ed27fc4e9da7d5fc09f2e1bc))

* ci: updating vidvec gravition Dockerfile ([`b1402b5`](https://github.com/tattle-made/feluda/commit/b1402b59d4efd834d42770940993a8050ae1b1c1))

* ci: removing duplicate run  commands in Dockerfile ([`f967496`](https://github.com/tattle-made/feluda/commit/f96749680bd002f067150340aff1c6ba2f520a1d))

* ci: audio worker staging github workflow ([`eec380a`](https://github.com/tattle-made/feluda/commit/eec380aaba6c04adc603a676bc52f6b411dd4d95))

* ci: video worker dockerfile for graviton ([`8554f3b`](https://github.com/tattle-made/feluda/commit/8554f3bf823414f64cf25cece5ff2add4ef2b127))

* ci: workflow dockerfile location change ([`d0826b8`](https://github.com/tattle-made/feluda/commit/d0826b8507e310977349062c254682763a28b90a))

* ci: fix location for video requirment file ([`96e0b87`](https://github.com/tattle-made/feluda/commit/96e0b870c8dba3360c2f4616fd38935ba98b4424))

* ci: workflow to push video worker to docker hub ([`594fc6c`](https://github.com/tattle-made/feluda/commit/594fc6c79f9632bd085f69b6598a16f9efba29a3))

* ci: workflow to push video worker to docker hub ([`730b808`](https://github.com/tattle-made/feluda/commit/730b808237193b16bf98e9e225435df69845ae85))

* ci: workflow to push video worker to docker hub ([`0d517c7`](https://github.com/tattle-made/feluda/commit/0d517c7c9362ce5d9844021fe9655b832c2267cd))

* ci: updating vid Dockerfiles ([`8c32315`](https://github.com/tattle-made/feluda/commit/8c323158bba28c7431867d7e86e469b9b654a1b2))

* ci: python version change in video dockerfile (#66) ([`aafde1c`](https://github.com/tattle-made/feluda/commit/aafde1c3c0a7e04546fa86a4cb3fa8e9e8739e83))

* ci: giving access to tests for video vec (#61) ([`5945004`](https://github.com/tattle-made/feluda/commit/5945004801c646d7fba6eab3018c6d5fddbd1c0a))

### Documentation

* docs: adding reference of audio cnn model ([`9d499be`](https://github.com/tattle-made/feluda/commit/9d499be767d0ce89f4d195068ef53c403b9610cc))

* docs: adding comments to the config-indexer ([`7bcbfca`](https://github.com/tattle-made/feluda/commit/7bcbfca5e39060602894ada922e81e4e3465f654))

* docs: tests documentation for YOLO and Tesseract operators (#47) ([`8eefb63`](https://github.com/tattle-made/feluda/commit/8eefb63454552c3bcc4613d63e5c5879d54cc1b6))

* docs: YOLO segementation operator (#46) ([`1a3da78`](https://github.com/tattle-made/feluda/commit/1a3da7800d6f7e839f5e4d8e0322c55997abe020))

* docs: documentation for tesseract ocr operator ([`37e3e30`](https://github.com/tattle-made/feluda/commit/37e3e30112e3312086ff8d259d5e773cd0cdfddd))

* docs: add Usage Case Studies ([`31400a6`](https://github.com/tattle-made/feluda/commit/31400a668e6aa8b6d66e4cddbab49fabd1d10634))

### Feature

* feat: worker for audio operator ([`becf40c`](https://github.com/tattle-made/feluda/commit/becf40cbd451da8305d7948a87eecc911476109a))

* feat: md5 operator ([`9e2d1be`](https://github.com/tattle-made/feluda/commit/9e2d1bec58105c3932bdf0db2e4e18d1a86c197c))

* feat: feluda store supports audio (#78)

* feat: feluda store supports audio

* fix: delete and refresh for ES

* dhore: profiling audio operator ([`f6987a6`](https://github.com/tattle-made/feluda/commit/f6987a6d3aa4ff018b5ebac248a4469437df80d3))

* feat: add poc multiprocess test ([`f43646b`](https://github.com/tattle-made/feluda/commit/f43646b4145af6cd8c6ea718be895ecbca77d271))

* feat: audio operator to extract embedding vectors (#59)

* feat: audio emebddings

* chore: deleting music files

* chore: renaming files

* docs: documentation for audio embedding operator

* docs: adding work to be done for the operator ([`484d5ae`](https://github.com/tattle-made/feluda/commit/484d5aed902b46d627c060625fad2a64a6246461))

* feat: c-profiling test for video vec (#60)

* feat: c-profiling test for video vec

* feat: test to find time taken for video vec ([`247f5db`](https://github.com/tattle-made/feluda/commit/247f5db90dc708f04bd0818f790d95c3e2c67a42))

* feat: add workflow to push vidvec specific operator to dockerhub ([`17e0d57`](https://github.com/tattle-made/feluda/commit/17e0d576492e379b2e4165e2b728868ab3fad455))

* feat: operator to detect objects using YOLO (#44)

* feat: operator to detect objects using YOLO

* test file comment main function

* chore: moving ultralytics install to opreator ([`17b9d10`](https://github.com/tattle-made/feluda/commit/17b9d107464f24875ca7008c4cf81cf0466e45d3))

* feat: operator to extract text in images using tesseract (#40)

* feat: opreator to detect text in images using tesseract
* chore: adding test images and making test multilingual ([`edec4a9`](https://github.com/tattle-made/feluda/commit/edec4a97763dd81e7dd7013833c690890563a1e9))

* feat: add license ([`a44e233`](https://github.com/tattle-made/feluda/commit/a44e233bf36fb4ad0d5bbd41a29523dc1f5364aa))

* feat: update docs ([`19a9217`](https://github.com/tattle-made/feluda/commit/19a9217a07319f18bbd051a8850d880b1998cf22))

* feat: add NER, add text search, add Not Implemented http response for raw query
- Added an operator to do Named Entity Recognition on non-english text
- Created a test and handler to respond to text queries
- Deferred the raw query search for later. It returns an HTTP response 501 now to denote that it hasnot been implemented ([`d57fb90`](https://github.com/tattle-made/feluda/commit/d57fb9065690ffa27d70f035c01900572976d968))

* feat: add pathways for /index depending on request content type ([`2f9f11f`](https://github.com/tattle-made/feluda/commit/2f9f11fee7f51d2c684f1c63322fd2c6b34d532c))

* feat: wip workers ready. testing pending ([`84f9f33`](https://github.com/tattle-made/feluda/commit/84f9f33a79037c095c31c6f9c8434665a3f408de))

* feat: indexing via worker in place ([`612593e`](https://github.com/tattle-made/feluda/commit/612593ebcc199e2f7a97223e6bdbf910095e15ba))

* feat: test end to end indexing for text, image and video ([`af6f144`](https://github.com/tattle-made/feluda/commit/af6f144db7d2c77307738fe367cbdcecb85cc1e3))

* feat: create generator for video vectors and store it in es ([`0208259`](https://github.com/tattle-made/feluda/commit/0208259d41bf8d98ece80044272f907e34168423))

* feat: index all 3 mediatypes via URL ([`bcb0237`](https://github.com/tattle-made/feluda/commit/bcb02379e359714b775ada264bbaea50d1386162))

* feat: remove stray files ([`55c39cf`](https://github.com/tattle-made/feluda/commit/55c39cf856f9a6a70f4aa70849145a493e716333))

### Fix

* fix: updating vidvec benchmark scripts ([`9aa4a50`](https://github.com/tattle-made/feluda/commit/9aa4a506d3936f21beeba4da0e8df8e879a0f4cd))

* fix: context manager handles vidoes ([`e8f36ce`](https://github.com/tattle-made/feluda/commit/e8f36cef56527ca6eb216c4be8b213d5a84cf8eb))

* fix: model is downloaded from github release ([`0c142df`](https://github.com/tattle-made/feluda/commit/0c142dfe0a1409bb2113961273be7fa2fcabeced))

* fix: video operator deletes file ([`8f97a95`](https://github.com/tattle-made/feluda/commit/8f97a9565186e51ad2bf679b1c71df1068ab3a6f))

* fix: video operator locaiton in Dockerfile ([`6d0e25d`](https://github.com/tattle-made/feluda/commit/6d0e25d60bfb6bb613e539104bac13337d97fced))

* fix: worker handles disconnection to MQ ([`b6a48f3`](https://github.com/tattle-made/feluda/commit/b6a48f3e35722a046d738b2c06441be4f8a4cf82))

* fix: cnn models works when saved on local machine ([`c86623d`](https://github.com/tattle-made/feluda/commit/c86623d100268226fca205a422f0094d569c47cf))

* fix: worker supports url and optimising on connection lost ([`80c122d`](https://github.com/tattle-made/feluda/commit/80c122d017c12072d93b1389933cae561701d081))

* fix: model fetched from local folder ([`ef512ef`](https://github.com/tattle-made/feluda/commit/ef512ef7119d0e7591a8fdf0f6be2ea63cf59fb6))

* fix: audio vec test supports media factory ([`41be124`](https://github.com/tattle-made/feluda/commit/41be1242038acc232e5de99c151fe3fe4bf23685))

* fix: video vec test supports media factory ([`bf727fd`](https://github.com/tattle-made/feluda/commit/bf727fd5fe3f9cd5e8c898c30ced4905240eaacc))

* fix: image vec test supports media factory ([`6e33270`](https://github.com/tattle-made/feluda/commit/6e33270f1ad6f918f5347ed90aae1fc806b0fd51))

* fix: Dockerfile location ([`a8ce31e`](https://github.com/tattle-made/feluda/commit/a8ce31e4ae614aad705c6ffaa2246f31263aeb5c))

* fix: server operator setup ([`c8a5bf8`](https://github.com/tattle-made/feluda/commit/c8a5bf8602500375bebffa932b7a551178741c95))

* fix: video es test (#87) ([`2670490`](https://github.com/tattle-made/feluda/commit/26704906b225ea1800a375d9f57c53e7a45e75c4))

* fix: url media link for index api test ([`089412a`](https://github.com/tattle-made/feluda/commit/089412a15badf351d8ef33538af9a4d2052a82b3))

* fix: index and search tests ([`ffc8efc`](https://github.com/tattle-made/feluda/commit/ffc8efc3274538d6a41320ff1906d593cb02950e))

* fix: search as client test (#83) ([`9855e96`](https://github.com/tattle-made/feluda/commit/9855e96eabfbff6f139f41051ec583af11136532))

* fix: graviton supported github runner ([`1ac59c9`](https://github.com/tattle-made/feluda/commit/1ac59c9c1fd881efbbda98a17f804cf08dee237b))

* fix: based image for graviton ([`e51ab2f`](https://github.com/tattle-made/feluda/commit/e51ab2f57cc66bbe6da2c0f90c580cbacacb65d7))

* fix: workflow file ([`8e74e9e`](https://github.com/tattle-made/feluda/commit/8e74e9e58a5240925e5b44c437882ca6c221c4d1))

* fix: video search (#52)

* chore: moving test files to a folder
* fix: video search
* docs: commenting TODO in search.py ([`af54ac0`](https://github.com/tattle-made/feluda/commit/af54ac0b7e2ef1afc139939e88cfc0f3fcc2dbfc))

* fix: search api as client ([`2573490`](https://github.com/tattle-made/feluda/commit/25734905ed04d6f302542ae152a3954d20e7ad31))

* fix: vid_vec_rep_res operator ([`0efc971`](https://github.com/tattle-made/feluda/commit/0efc971085d28d49c0822db9760ce9a1cd78f996))

* fix: index image api ([`bc1a56a`](https://github.com/tattle-made/feluda/commit/bc1a56a04356b8007b880fa52e2e8d9655ec1df9))

* fix: image_vec_rep_resnet operator ([`7b3b419`](https://github.com/tattle-made/feluda/commit/7b3b419e549faa92de7d6b7cf9804175ff0da501))

* fix: elastic search test ([`0326407`](https://github.com/tattle-made/feluda/commit/03264072021a7f8797086ec824d7869b5d6dc272))

* fix: uncommenting ES_HOST code ([`144c828`](https://github.com/tattle-made/feluda/commit/144c828732cbe0a4ff8594ae52570a438d89e652))

* fix: server is up and running ([`29b6100`](https://github.com/tattle-made/feluda/commit/29b610073377104db866963206c61b7f6175ac75))

* fix: removed trailing comma ([`a687377`](https://github.com/tattle-made/feluda/commit/a6873775fc0355de7332e1c06b91d7656d999e22))

* fix: add separator between filenames ([`184022f`](https://github.com/tattle-made/feluda/commit/184022f092c8a0ac491ebd913c6eb70abc007758))

### Refactor

* refactor: config file for video worker ([`66cd139`](https://github.com/tattle-made/feluda/commit/66cd13979cb0c3d9c4547127b8521182fe28da68))

* refactor: moving tests to sub-folders ([`6837b89`](https://github.com/tattle-made/feluda/commit/6837b8916ec0164b6af4ed099f203a86f522659f))

* refactor: rebasing worker branch to master ([`1656ece`](https://github.com/tattle-made/feluda/commit/1656ece2f5c55b675f70a9fe8face366b68b39ca))

* refactor: core module import ([`07cbb11`](https://github.com/tattle-made/feluda/commit/07cbb11f534924a401495506804bef47a3554ab1))

* refactor: removing api folder ([`91c797b`](https://github.com/tattle-made/feluda/commit/91c797b1d2f60664344f77167418aeb9f692dbf8))

* refactor: vidvec locust es files ([`6d90ded`](https://github.com/tattle-made/feluda/commit/6d90deda7f38faef34af8f572bbf1bc72fda3c22))

* refactor: vidvec benchmark files ([`4daa789`](https://github.com/tattle-made/feluda/commit/4daa789f82c21dcbcd8385a551c7a86be6e1e858))

* refactor: moving test files ([`6e62215`](https://github.com/tattle-made/feluda/commit/6e622151ec6116931374f52a1e42121cf9aed772))

* refactor: moving tests files ([`2eb932d`](https://github.com/tattle-made/feluda/commit/2eb932d55686480a9b3fe542fe2bbb5c5b2db092))

* refactor: benchmark test sh file (#64)

* refactor: benchmark test sh file

* ci: dockerfile udpate for benchmark.sh

* chore: echo statements for benchmark file ([`37e768a`](https://github.com/tattle-made/feluda/commit/37e768a38af2dcc169c395dace49bd708eeeaef1))

* refactor: cleanup deprecated thigns. ([`4c67853`](https://github.com/tattle-made/feluda/commit/4c67853e75b8511cfb89158a358f60523851b138))

* refactor: added comment ([`a8053ba`](https://github.com/tattle-made/feluda/commit/a8053ba4ebc0ce98ea8df44e2ec7504299fcbb4e))

* refactor: cleaned up ([`e7515c0`](https://github.com/tattle-made/feluda/commit/e7515c032171b9f97f0c31310f2bff3ad9e3582a))

* refactor: debugging statements ([`fddb01a`](https://github.com/tattle-made/feluda/commit/fddb01a852cba2043bffd7b33d680359d4a308be))

* refactor: source id field ([`6dfc8d3`](https://github.com/tattle-made/feluda/commit/6dfc8d327936cb5d39d4cb3d87084132c8bef26d))

### Test

* test: benchmarking scripts for audiovec operator ([`12685bd`](https://github.com/tattle-made/feluda/commit/12685bd7d089e281c2b6fcac736b6063bf8bfa2e))

* test: md5 hash supports media factory ([`a75751c`](https://github.com/tattle-made/feluda/commit/a75751c571af8cadc49d7667f7dc9b7074099c5b))

* test: media factory unit test ([`d2914d1`](https://github.com/tattle-made/feluda/commit/d2914d1d2da28c5aaf131183d4714e62b1daffea))

* test: worker to queue and index video files (#84)

* refactor: small improvements

* test: worker to queue and index video vec ([`6eaf19b`](https://github.com/tattle-made/feluda/commit/6eaf19b39298762b6f9a3f34e50858d7314d02e6))

### Unknown

* Merge pull request #119 from tattle-made/hotfix

Hotfix ([`aa0d296`](https://github.com/tattle-made/feluda/commit/aa0d296456de50d83b7146252c1d3d7a2e956c5a))

* Merge pull request #116 from aatmanvaidya/audio-worker-ci-tag-change

ci: audiovec worker staging dockerhub tag change ([`71c43c8`](https://github.com/tattle-made/feluda/commit/71c43c88e58c01e43647607d12da35095eb94fed))

* Merge pull request #115 from aatmanvaidya/bench-graviton

ci: audiovec benchmark graviton dockerfile ([`3ca919c`](https://github.com/tattle-made/feluda/commit/3ca919c6f8bb8e89e9984ac750b4529fffe74955))

* Merge pull request #114 from aatmanvaidya/video-worker-config

refactor: config file for video worker ([`31cfe77`](https://github.com/tattle-made/feluda/commit/31cfe77cf4137cabadbb666eff44c5fd35568c7f))

* Merge pull request #118 from tattle-made/hotfix

Hotfix ([`6cdeb25`](https://github.com/tattle-made/feluda/commit/6cdeb258fe75abbff5d240f61ab3f2268ce5dbb5))

* Merge pull request #117 from duggalsu/github_workflow_merge_dev

ci: Add automated semantic versioning ([`4a12794`](https://github.com/tattle-made/feluda/commit/4a1279437ca826bbf476535c5abdd99262fdc2a5))

* Merge pull request #113 from tattle-made/hotfix

Hotfix ([`9de3594`](https://github.com/tattle-made/feluda/commit/9de3594dccf29ecea2e28dd5f373b0b72e42a18f))

* Merge pull request #112 from aatmanvaidya/video-bench-update

fix: updating vidvec benchmark scripts ([`c766038`](https://github.com/tattle-made/feluda/commit/c766038bf9b71efcc1c1fd8df6eff675ea72bf81))

* Merge pull request #111 from aatmanvaidya/audio-benchmark

test: benchmarking scripts for audiovec operator ([`4bf9dab`](https://github.com/tattle-made/feluda/commit/4bf9dab091bce3eca0077b235b2d7f0346934a9f))

* Merge pull request #110 from aatmanvaidya/audio-worker-github-workflow

ci: audio worker staging github workflow ([`9e11c03`](https://github.com/tattle-made/feluda/commit/9e11c039728f85cbf34fc4c8bb89ae77c390e8b4))

* Merge pull request #109 from aatmanvaidya/audio-worker

feat: worker for audio operator ([`23ff0f0`](https://github.com/tattle-made/feluda/commit/23ff0f080a939513eb97ed6a06c03fbdca0595e1))

* Merge pull request #108 from aatmanvaidya/video-graviton

ci: video worker dockerfile for graviton ([`fed8e23`](https://github.com/tattle-made/feluda/commit/fed8e23ffbe141d46ac880e6074b4063652ea02b))

* Merge pull request #93 from aatmanvaidya/md5-test-fix

test: md5 hash supports media factory ([`b0685a6`](https://github.com/tattle-made/feluda/commit/b0685a669076b44f91d254016d36f4cb4d475e91))

* Merge pull request #106 from aatmanvaidya/audio-cnn-fix

fix: audio operators uses function from a local folder ([`da3d37d`](https://github.com/tattle-made/feluda/commit/da3d37dd9fc6bdf78919ea0b0452f4e6a8e0b68f))

* Merge pull request #107 from aatmanvaidya/video-op-fix

fix: context manager handles vidoes ([`586b0c0`](https://github.com/tattle-made/feluda/commit/586b0c051c4ab9b252b40fa58d614a62eea760fa))

* Merge pull request #105 from tattle-made/hotfix

Hotfix ([`4ae4219`](https://github.com/tattle-made/feluda/commit/4ae4219055f5ccd142ac5a25a294cf5a110da573))

* Merge pull request #104 from duggalsu/github_workflow_pr

GitHub workflow pr ([`cda6bbb`](https://github.com/tattle-made/feluda/commit/cda6bbbd80cbef0ad68a62ea12bda041cf0d0517))

* - Disabled failing tests ([`b7ace62`](https://github.com/tattle-made/feluda/commit/b7ace6284b6aa1797bdb50ceb2fe670ab2626ada))

* - Enabled failing tests ([`e7df52c`](https://github.com/tattle-made/feluda/commit/e7df52c4b62dcdded29c317a21b877c035e93933))

* - Modified failure condition ([`6c22a62`](https://github.com/tattle-made/feluda/commit/6c22a623435ff88d64994eb82ac2964e314482c2))

* - Added echo output ([`4e3d04e`](https://github.com/tattle-made/feluda/commit/4e3d04e3173312a5047a4e9e1e836373ca0092cc))

* - Skipped index api tests ([`87ba7bb`](https://github.com/tattle-made/feluda/commit/87ba7bb1902743a699e6c4863a1a339139731038))

* - Added sut output and failure condition ([`7f2022e`](https://github.com/tattle-made/feluda/commit/7f2022e8ba73ccc0c6517fd2f77a26c0ed17b965))

* - Disabled failure check ([`d7e2aa4`](https://github.com/tattle-made/feluda/commit/d7e2aa42050c18d1ba5b09d17ff5f0fc72b04d63))

* - Added log outputs and failure condition ([`ceea228`](https://github.com/tattle-made/feluda/commit/ceea228818d033e239263dc9139a2c6723c2cb68))

* - Enabled failing tests for testing PR workflow ([`cd953a4`](https://github.com/tattle-made/feluda/commit/cd953a4525edff17bf9bdb1a6ef46e0b666881bd))

* - Modified pr workflow to use test.env
- Added test.env
- Added test.env inclusion in gitignore ([`cd37c9d`](https://github.com/tattle-made/feluda/commit/cd37c9d0b2f703064811268d72188970fe5762de))

* - Skipped search and index api tests ([`469d95e`](https://github.com/tattle-made/feluda/commit/469d95ed6df1f8300632bae1f456fd0b6885a980))

* - Added nose to requirements ([`282e7f6`](https://github.com/tattle-made/feluda/commit/282e7f674dc0a80f1e14b0d1154c5830ac79bbfc))

* - Disabled image vec operator in config-server.yml
- Disabled audio testing ([`026e92f`](https://github.com/tattle-made/feluda/commit/026e92fedc31fca010458b9c179efb243a7c9506))

* Add github PR testing workflow
- Added github pr workflow yaml
- Added ci pr test dockerfile
- Added ci pr docker compose file
- Added ci dockerfiles to gitignore ([`c857181`](https://github.com/tattle-made/feluda/commit/c857181ab8345d4528937a3873e4f0195ea1640f))

* Merge pull request #102 from aatmanvaidya/vid-ci-5

fix: video operator locaiton in Dockerfile ([`d6ed2a3`](https://github.com/tattle-made/feluda/commit/d6ed2a39304f8cd42cfff352470ad2963554b177))

* Merge pull request #103 from tattle-made/hotfix

Hotfix ([`3f41df9`](https://github.com/tattle-made/feluda/commit/3f41df9c2a688bc94de093a5c3e2eeadff8659e6))

* Merge pull request #101 from aatmanvaidya/vid-ci-4

ci: workflow dockerfile location change ([`b7d9ab2`](https://github.com/tattle-made/feluda/commit/b7d9ab287f3cb99f96ea4b3f54f5e9a5520d7c60))

* Merge pull request #100 from aatmanvaidya/vid-ci-2

ci: fix location for video requirment file ([`92a103e`](https://github.com/tattle-made/feluda/commit/92a103eba924b475c230499dc5de266a18255894))

* Merge pull request #99 from dennyabrain/local-hotfix

Local hotfix reconciling with main ([`79659eb`](https://github.com/tattle-made/feluda/commit/79659eb3a1f01205e26ba4443cca53e216af2fd7))

* Merge pull request #98 from tattle-made/hotfix

Hotfix ([`579b7ea`](https://github.com/tattle-made/feluda/commit/579b7ea7c65da39949a81d4768d8f4fc00f01e1b))

* Merge pull request #96 from aatmanvaidya/worker-ci

ci: workflow to push video worker to docker hub ([`07b609c`](https://github.com/tattle-made/feluda/commit/07b609c1898c88d8aab225ec63ccaca356ea5847))

* Merge pull request #95 from aatmanvaidya/worker-improve

fix: video worker handles disconnection to RabbitMQ ([`9ce22a2`](https://github.com/tattle-made/feluda/commit/9ce22a2f591b699c15704cc0e1111b2bdb46a57f))

* Merge pull request #94 from aatmanvaidya/tests-move

refactor: moving tests to sub-folders ([`bf24df2`](https://github.com/tattle-made/feluda/commit/bf24df2bafbfe4453b005c76989ac81ed27f2664))

* Merge pull request #80 from duggalsu/enable_rabbitmq

Enable RabbitMQ ([`e055a24`](https://github.com/tattle-made/feluda/commit/e055a24e934960b46df783e20e300c926e76c595))

* Enable RabbitMQ
- Enabled rabbitmq disabled in PR https://github.com/tattle-made/feluda/pull/74/files
- Updated rabbitmq version ([`8fb6d1f`](https://github.com/tattle-made/feluda/commit/8fb6d1fd32f132cfc1ee93e1f9cfe33f761580a9))

* Merge pull request #79 from duggalsu/benchmark_es

Add ElasticSearch benchmarking ([`03915d3`](https://github.com/tattle-made/feluda/commit/03915d3c893bcf2def3b5fd836a60db950425bef))

* Add ElasticSearch benchmarking
- Added locust out files to gitignore
- Fixed import issues in video operator
- Fixed file size limit to 10mb in video operator
- Optimized video operator to run with constant memory usage
- Fixed UnboundLocalError in es_vec.py
- Updated flask_cors package for locust compatibility
- Added locust package to requirements.in
- Regenerated feluda core requirements.txt
- Added tests for indexing and searching videos in elastic search
- Added video operator ES search benchmark locust file
- Added python file to index videos as init for ES load testing
- Added bash script to perform video load testing ([`1e6b470`](https://github.com/tattle-made/feluda/commit/1e6b470a1e437494c2a41e0ce96d95d0c065aac8))

* [WIP] test: evaluating audio vec ES index and search (#77)

* test: evaluating audio vec ES index and search

* docs: delete stored documents ([`ad94ad7`](https://github.com/tattle-made/feluda/commit/ad94ad745d85c734fe1c7671ce43c4f2a9e28876))

* Merge pull request #76 from duggalsu/add_arch_to_docker_tag

Added architecture to docker tag name ([`812cd1d`](https://github.com/tattle-made/feluda/commit/812cd1dfef87141cad3af846fc2dc872a16d5cc9))

* - Added architecture to docker tag name ([`17c24d5`](https://github.com/tattle-made/feluda/commit/17c24d501c14e4c6a1765fac1182c005fd5b40ac))

* Merge pull request #75 from duggalsu/fix_docker_tag_issue

Fix tag name issue ([`f4905bf`](https://github.com/tattle-made/feluda/commit/f4905bfd38798406fb54646de18a956205e79d26))

* Fix tag name issue
- Modified tag naming syntax in github actions ([`54fea21`](https://github.com/tattle-made/feluda/commit/54fea21c9bee33152b84b6d49c043477bac61062))

* Merge pull request #74 from duggalsu/config_changes

Update configs ([`7ca754d`](https://github.com/tattle-made/feluda/commit/7ca754d8f1a18b7072865ce6b449d00ba1676c87))

* Update configs
- Disabled feluda reporter from docker compose file
- Disabled rabbitmq
- Removed operator specific packages from feluda core
- Regenerated feluda core requirements
- Enabled debian bullseye in core feluda for AWS Graviton support
- Removed apt-get packages from feluda core dockerfile
- Updated torch version in vid vec requirements.in
- Added graviton dockerfile
- Updated vid vec github action to create dockerfile per arch ([`e005e32`](https://github.com/tattle-made/feluda/commit/e005e3226f143610ed322803a4ad4ecd9ba69fc9))

* Merge pull request #72 from duggalsu/add_pytorch_arch_conditional

Add pytorch arch conditional ([`136894a`](https://github.com/tattle-made/feluda/commit/136894abf8f1f20c3c81a15fea0e0a76a06b534e))

* - Revert base image for Graviton compatibility ([`2985432`](https://github.com/tattle-made/feluda/commit/2985432388677e33951aa6ad388e00a4229a1fc0))

* Add arch conditional pytorch install
- Added conditional for building multi-arch cpu pytorch ([`1ecc864`](https://github.com/tattle-made/feluda/commit/1ecc864d5c1a473c51cd2512e49cb9e80169eb62))

* Merge pull request #71 from duggalsu/fix_vid_vec_graviton_dockerfile

Fix Graviton commands ([`72bd171`](https://github.com/tattle-made/feluda/commit/72bd171851034467d8455c3a023ccd257b0290a1))

* Fix Graviton commands
- Fixed AWS Graviton opt commands in dockerfile ([`f3893aa`](https://github.com/tattle-made/feluda/commit/f3893aa71cc6252a1f387aeb056f51b210dfbabd))

* Merge pull request #70 from duggalsu/fix_github_actions_docker_platforms

Fix Unexpected input(s) &#39;platforms&#39; ([`09c320d`](https://github.com/tattle-made/feluda/commit/09c320d6229fcbe11bc4c26207d975cfd859e2f3))

* Fix Unexpected input(s) &#39;platforms&#39;
- Fixed platforms issue ([`6fb2c89`](https://github.com/tattle-made/feluda/commit/6fb2c899f43e761a47476e8aa1665b4eaec8affb))

* Merge pull request #69 from duggalsu/fix_github_actions_docker

Fix docker github action ([`e74f388`](https://github.com/tattle-made/feluda/commit/e74f388a40781c10f82380102f770381c1b6947d))

* Fix docker github action
- Added custom node version
- Fixed node12 and node16 deprecation warnings by upgrading actions
- Fixed set-output deprecation warning ([`8dac771`](https://github.com/tattle-made/feluda/commit/8dac771413f794bb81169fa209e5b693117a4b4e))

* Merge pull request #68 from duggalsu/opt_pytorch_graviton

Optimize docker for multi-arch builds ([`575b6c4`](https://github.com/tattle-made/feluda/commit/575b6c44f8167122b0d37512419631ef462a6b76))

* - Fix num_processes flag ([`c22bc58`](https://github.com/tattle-made/feluda/commit/c22bc5891c94d72541874dc6173fd00ce6a4a53e))

* Optimize docker for multi-arch builds
- Added pytorch optimization for AWS graviton in dockerfile
- Modified requirements.txt to work with multi-arch support
- Modified docker vid vec github action with multi-arch build support ([`3e2707f`](https://github.com/tattle-made/feluda/commit/3e2707f21e776f132a5fb9f9dec7422d3be0cc29))

* fix ([`9a10d9a`](https://github.com/tattle-made/feluda/commit/9a10d9aed90e3c8163bb921cc5c5fc0fc1a18e35))

* revert: python version (#67) ([`4950ee7`](https://github.com/tattle-made/feluda/commit/4950ee7676019772f17855984fff810db93ea61b))

* Merge pull request #63 from duggalsu/fix_operator_issue

Fix modular operator issues ([`04c92f4`](https://github.com/tattle-made/feluda/commit/04c92f43f6d92c9fbf667d275d61607bf905bdfa))

* Fix modular operator issues
- Updated shebang in shell scripts
- Updated operator dockerfiles
- Updated requirements ([`d850c05`](https://github.com/tattle-made/feluda/commit/d850c056fd15fcb07ea67834a19291d72411bb4a))

* Merge pull request #62 from duggalsu/benchmark_scripts

Benchmark scripts ([`b4c4eca`](https://github.com/tattle-made/feluda/commit/b4c4eca3a89ea09c21491fdabc656f96ca1bb05a))

* - Added shebang to all scripts ([`2ea4d1b`](https://github.com/tattle-made/feluda/commit/2ea4d1b225561580f861872da82eea7c59a41d29))

* - Added chmod executable for all scripts in image and vid dockerfiles ([`fcc8a68`](https://github.com/tattle-made/feluda/commit/fcc8a68b74192cbff1fe7f4986cebec5f89e1fd6))

* Add benchmarking scripts
- Added image vec python script
- Added image memray benchmarking shell script
- Added image pyinstrument benchmarking shell script
- Added video vec python script
- Added video memray benchmarking shell script
- Added video pyinstrument benchmarking shell script ([`ee7d338`](https://github.com/tattle-made/feluda/commit/ee7d338405fd27505d922fdb2e9bd20683db191d))

* Merge pull request #58 from duggalsu/docker_opt

Create and optimize Dockerfiles ([`7ece59c`](https://github.com/tattle-made/feluda/commit/7ece59cec4d6c5e5082c3c49ad7f0690808bb602))

* - fixed typo in readme ([`267d13e`](https://github.com/tattle-made/feluda/commit/267d13ebb2ce1cb3a7774523c424f1fa955f8783))

* - Updated readme
- Added --no-cache-dir for pip install in dockerfiles
- Removed vim curl single install command from core dockerfile
- Removed torch, torchvision as core feluda dependency
- Added numpy as core feluda dependency
- Recreated core requirements.txt
- Modified test urls ([`7b0cf99`](https://github.com/tattle-made/feluda/commit/7b0cf99454ba598f9fc33f625df2d89d0671e4dc))

* Create and optimize Dockerfiles
- Optimized feluda core Dockerfile
- Added image_vec_rep_resnet operator Dockerfile
- Added vid_vec_rep_resnet operator Dockerfile
- Updated boto3 to fix dependency incompatibility
- Fixed deprecation warning for resnet18
- Updated image_vec_rep_resnet requirements.in
- Recreated image_vec_rep_resnet requirements.txt
- Updated nltk version in text_vec_rep_paraphrase_lxml for compatibility
- Recreated text_vec_rep_paraphrase_lxml requirements.txt
- Removed unused packages for video operator
- Fixed os as global import in video operator
- Removed ffmpeg dependency in video operator and feluda core
- Recreated video operator requirements.txt
- Removed unused packages from feluda core
- Recreated feluda core requirements.txt ([`85a7e6d`](https://github.com/tattle-made/feluda/commit/85a7e6d35f817d94aa7cc4c3866e65d155cc9eb9))

* Merge pull request #56 from duggalsu/cpu_profiling

Add cpu profiling and optimize operator ([`c350792`](https://github.com/tattle-made/feluda/commit/c350792db1ffcb9c53149ea42f68adf5f4b0cd07))

* Add cpu profiling and optimize operator
- Added pyinstrument for cpu profiling
- Added gitignore requirement for pyinstrument
- Disabled compress function for operator
- Removed ffmpy dependency as it is not required now ([`95a2959`](https://github.com/tattle-made/feluda/commit/95a295981488b627aa4710034e58917f6ac1d007))

* Merge pull request #55 from duggalsu/mem_profiling

Add memory profiling ([`9d7fb86`](https://github.com/tattle-made/feluda/commit/9d7fb863c2599eb81dc28131b7dbbfb972c42cac))

* Add memory profiling
- Added memray package for memory profiling
- Recreated requirements.txt
- Fixed typo in operator
- Added memray output bin and html files to gitignore ([`69ab511`](https://github.com/tattle-made/feluda/commit/69ab5111f91ce4dbeb5ad8fcfedca119646155a6))

* Merge pull request #54 from duggalsu/test_documentation

Update documentation ([`a29e7a7`](https://github.com/tattle-made/feluda/commit/a29e7a7ca273fbab0c972f86fe12ad00192b9e70))

* - Updated readme
- Updated gitignore with sonarqube exclusion ([`375c1b9`](https://github.com/tattle-made/feluda/commit/375c1b9b203184d8d14c56c492f27419f3893596))

* Merge pull request #50 from duggalsu/deprecate_ner_extraction_operator

Deprecate NER Extraction operator ([`8e55226`](https://github.com/tattle-made/feluda/commit/8e552260adcffcec31897f6836fc793c18be62ca))

* Deprecate NER Extraction operator
- Deleted the ner extraction python file as packages are not maintained
- Deleted operator requirements.in
- Deleted operator requirements.txt ([`7b27aec`](https://github.com/tattle-made/feluda/commit/7b27aec64a2abf33a0f0bc18547f37ae6fe1393e))

* - Updated readme
- Updated required operators in config-server.yml
- Downgraded package in vid_vec_rep_resnet_requirements for compatibility
- Modified handler.py for compatibility with current operators
- Updated packages in core requirements to match operator versions ([`77f867c`](https://github.com/tattle-made/feluda/commit/77f867cf9086d105903df0d72736e480a5dc42eb))

* - Updated readme
- Removed package install scripts from operators
- Created operator-specific requirements.in
- Generated operator-specific requirements.txt ([`f276855`](https://github.com/tattle-made/feluda/commit/f276855ee993d4854a37b441dcf427c8010b0c5e))

* - Updated readme
- Moved all `operator` package installs to `requirements.in`
- Deleted `operator/installer.py` script for harm reduction
- Recreated `requirements.txt` ([`acf8b73`](https://github.com/tattle-made/feluda/commit/acf8b730640ec7db899707dc98a32baa56c5fff5))

* - Removed extra newline from docker-compose file
- Updated flask debug settings for new version in Dockerfile
- Updated package sentencepiece to work with cp311 ([`c60cf42`](https://github.com/tattle-made/feluda/commit/c60cf42fc4da11c3409ea2f584ec4ab5d97c96c3))

* - Updated python docker image ([`c05de12`](https://github.com/tattle-made/feluda/commit/c05de12e697fc9c0128dab0d39742d8b12cd2cff))

* Update Feluda
- Updated readme instructions
- Fixed docker-compose file issues
- Updated and pinned packages to work with cp311, fixes from `pip-audit`
- Recreated `requirements.txt` ([`6d91094`](https://github.com/tattle-made/feluda/commit/6d9109484b33ee55d52d715e5f0b7741bfe8aa09))

* Merge pull request #43 from aatmanvaidya/docs-ocr

docs: documentation for tesseract ocr operator ([`79d67ee`](https://github.com/tattle-made/feluda/commit/79d67ee01653aa52dc2aba38efc34ad4f2f5b1de))

* Create privacy_policy.md ([`ac254d1`](https://github.com/tattle-made/feluda/commit/ac254d164dcfb54a1fc22bf11069c62a3a620af2))

* Update README.md ([`2aad47e`](https://github.com/tattle-made/feluda/commit/2aad47e0a3edfc2cebc7a25361e0603075aed25f))

* fix :  renamed env variable for kosh api ([`f6bb56c`](https://github.com/tattle-made/feluda/commit/f6bb56c9eeb838dfcea5348209f990fb6dd471cb))

* chore : testing ci ([`72c6c4a`](https://github.com/tattle-made/feluda/commit/72c6c4a870685e08ba047795a8074a33181f6162))

* feat : added deploy script to docs ([`3a8187b`](https://github.com/tattle-made/feluda/commit/3a8187ba500cf91e7966dc0716bbdf0b09ddcda4))

* chore : testing ci ([`7e626c1`](https://github.com/tattle-made/feluda/commit/7e626c1acf1092437cc52082ac7c53e6e52d992d))

* chore : testing ci ([`c6424cf`](https://github.com/tattle-made/feluda/commit/c6424cfd921dc2f5f8bcf5201daf53cdaa7f5e0d))

* chore : testing ci ([`7e3d836`](https://github.com/tattle-made/feluda/commit/7e3d836022efae3ef063459507a756c5bca00d5e))

* feat : misc
- add support for raw query of es.
- add ci workflow. ([`88a6607`](https://github.com/tattle-made/feluda/commit/88a6607d3edb6eea048d38967de6412add06749f))

* fix : string to dict conversation in reporter. ([`8f1433a`](https://github.com/tattle-made/feluda/commit/8f1433a85b2189f6742b02c4b2d209ec856b1fda))

* fix : resolve issues arising from using e_kosh_id as the key in store as opposed to id or post_id ([`d4aabba`](https://github.com/tattle-made/feluda/commit/d4aabbae7e504846fdedb75406ba0c7790383c9b))

* feat : add debug support for store and queue. enable shared networking with kosh. ([`3c30e6e`](https://github.com/tattle-made/feluda/commit/3c30e6ea10e33c2be2dba12a2d9557793b029227))

* Merge branch &#39;master&#39; of github.com:tattle-made/tattle-api ([`3919dbd`](https://github.com/tattle-made/feluda/commit/3919dbd15a1ea9ebcecdf1b34cb465a3aab504cf))

* feat : add ner support, add debug cli and its documentation ([`8757c60`](https://github.com/tattle-made/feluda/commit/8757c60c8587d85a2cb0b916856c65e72760ddb8))

* GP | added CORS support, fixed image search ([`caace21`](https://github.com/tattle-made/feluda/commit/caace219b51fd5ad54d95155b64bbbe6ce0c1d92))

* fix : make datasource_id and client_id optional ([`8873c9e`](https://github.com/tattle-made/feluda/commit/8873c9e707d09c8bb19fe4c51d2314ff301361f5))

* fix : docker compose debug changes ([`bdceed1`](https://github.com/tattle-made/feluda/commit/bdceed1238c73004c5ca50ff75728fba9d175613))

* fix : merge conflict ([`4fe2143`](https://github.com/tattle-made/feluda/commit/4fe2143156c93f6e99a2a1f89a1ecd4e4537f3b5))

* tmp ([`2a37de0`](https://github.com/tattle-made/feluda/commit/2a37de089615496b8efd59e9d86337cbc4fce0bf))

* doc: clean up feluda and document config module. ([`edeb72e`](https://github.com/tattle-made/feluda/commit/edeb72e3064d75c76964de13389ffe75560e2238))

* doc :  add todo to convert an image search model into an operator ([`4266717`](https://github.com/tattle-made/feluda/commit/42667175befa62a9fc94566de2d4e1f014be28de))

* feat : test end to end index endpoint ([`b3e5b12`](https://github.com/tattle-made/feluda/commit/b3e5b1233da330370f1f00901e331ac8c7fa8765))

* refactor : separate feluda core code and user code ([`0918507`](https://github.com/tattle-made/feluda/commit/09185072cc54e1fd76cf23b7be1b2d659d027840))

* doc : add overview, operators, architecture, etc. ([`0961e59`](https://github.com/tattle-made/feluda/commit/0961e59a2fa49c2d68c29080bf7e50354cd255f9))

* doc : add gatsby site for documentation. ([`b5c519a`](https://github.com/tattle-made/feluda/commit/b5c519a5e93ffbc069b74579c09406cde1d96102))

* fix : rename operator variable ([`839adfa`](https://github.com/tattle-made/feluda/commit/839adfa705cc79550a3a41228f4052e7c7b2d0c6))

* doc : add endpoint and overview
refactor : rename feature to endpoint ([`68f9d5c`](https://github.com/tattle-made/feluda/commit/68f9d5cac0e2b9def54a7034572f1d5624192b62))

* fix: ([`0a02845`](https://github.com/tattle-made/feluda/commit/0a02845bb286a3c469b8e8d46b3b8a4a5e36a769))

* doc: add caveate about environment variables ([`0da5097`](https://github.com/tattle-made/feluda/commit/0da5097424200b7020e10d7bd9b29ed372c9e5ea))

* feat  : add type safety for config ([`be08274`](https://github.com/tattle-made/feluda/commit/be08274ab832453b055d8f7f9daa976194b97f33))

* feat : add logger and documentation. add queue ([`3a80079`](https://github.com/tattle-made/feluda/commit/3a800793e65ad72dbf640a1f05b44dd00f9b988d))

* feat : add frontmatter to documentation pages ([`2a08202`](https://github.com/tattle-made/feluda/commit/2a082027c96ef96669f0849983af4f3b556a51d4))

* dmp ([`a198747`](https://github.com/tattle-made/feluda/commit/a198747c55dad4a3a6da0b6fd88bdc6c78cc8824))

* feat : add test for /represent image ([`1e3d8d1`](https://github.com/tattle-made/feluda/commit/1e3d8d1b40c45e76afec0b299a41777b8e48d2f3))

* doc : add documentation for operators ([`a4bceda`](https://github.com/tattle-made/feluda/commit/a4bcedac77c1f5c9c7899c75c7bf16d959d4d9b0))

* refactor : move operator config up as standalone in config.yml. remove index and search realted config. ([`170f838`](https://github.com/tattle-made/feluda/commit/170f838eace6afa345993aa058e0ae601f724870))

* feat : debugging ready ([`38525c5`](https://github.com/tattle-made/feluda/commit/38525c54a8f2c2410d71408a743d9a5244acb937))

* feat : set up 3 endpoints for indexing media ([`1efc4fd`](https://github.com/tattle-made/feluda/commit/1efc4fd37dcf08f8c8b7b0676c6c6d04025431d8))

* testing API endpoints with json and file sent in one request ([`08204b8`](https://github.com/tattle-made/feluda/commit/08204b87d0ba99404bd5c9abbbbb2e89f1abd52a))

* dmp ([`14b7845`](https://github.com/tattle-made/feluda/commit/14b78454e99cf7601ac03e71359929c51be2de48))

* fix : update README ([`56f42f0`](https://github.com/tattle-made/feluda/commit/56f42f0c807203cb8082bbfc505b8688d5660f37))

* wip ([`a8409ab`](https://github.com/tattle-made/feluda/commit/a8409abda7eef4802256eba75e2fba71c22ecb68))

* temp ([`2fcb3b0`](https://github.com/tattle-made/feluda/commit/2fcb3b03d013e524d2c582fad69e67b1c4ce7f50))

* dmp ([`157f7ed`](https://github.com/tattle-made/feluda/commit/157f7ed6b28855dd19212e2d6c23f645ce0b5ae5))

* dmp ([`931850f`](https://github.com/tattle-made/feluda/commit/931850fe8efefaf39688c30b67c2d84a4faea3d6))

* change package versions to resolve conflicts ([`e13cb92`](https://github.com/tattle-made/feluda/commit/e13cb92322e2a9fd07df5d21576ac84ae85eb115))

* add video indexing example &amp; docker build info ([`c439ccc`](https://github.com/tattle-made/feluda/commit/c439ccc203ef24114e87acc81f566fe136e6cdf3))

* increased number of search results returned by API ([`5594278`](https://github.com/tattle-made/feluda/commit/55942788f85469804543029e1a6de7a7441e6a6a))

* added bulk indexing info ([`9252902`](https://github.com/tattle-made/feluda/commit/925290295721cfb0bbe4a1996ccf0a27fcab519d))

* add more elasticsearch info ([`47f2104`](https://github.com/tattle-made/feluda/commit/47f2104b81aa4a49eeeabb822650f71beae88100))

* updated ([`c9bd498`](https://github.com/tattle-made/feluda/commit/c9bd49813d3d98816b70d65aff61fd6342513806))

* add explanatory comment for query size ([`d764fe1`](https://github.com/tattle-made/feluda/commit/d764fe189555e50784749165b6e1f2fd3847f6ce))

* expand docstring for sentencer transformer function ([`3122078`](https://github.com/tattle-made/feluda/commit/312207823000e0fc06f2fae7b124b868d1ee7559))

* comment out index deletion &amp; add warning ([`3887661`](https://github.com/tattle-made/feluda/commit/3887661494ea8289f2599a648721505603a7155e))

* deprecate mongo, remove its dependencies ([`f3e4e28`](https://github.com/tattle-made/feluda/commit/f3e4e28a9b00fdc285a3455c721dd7dd9dffd929))

* deprecate mongo, remove its dependencies ([`69d3970`](https://github.com/tattle-made/feluda/commit/69d3970e041ac8b644514d0dcfa6f5dccbca769e))

* return top 3 search hits in more readable format ([`c943828`](https://github.com/tattle-made/feluda/commit/c9438282ae75fb8439d4637536fde5d3bef86a29))

* changed text vector size ([`edaeead`](https://github.com/tattle-made/feluda/commit/edaeeadf947a5740c81ae07290ec0733a0e17622))

* added sentence transformers library ([`6615f95`](https://github.com/tattle-made/feluda/commit/6615f95407c49e9d2ff5870d442c31e9c5aa23b8))

* replaced word2vec with sentence transformer embeddings ([`0a92b67`](https://github.com/tattle-made/feluda/commit/0a92b670af9a133ce50931723a203c4678fad4d5))

* word2vec db install files with lang ids fixed ([`ae5fb01`](https://github.com/tattle-made/feluda/commit/ae5fb0132bff16bdaebfccbc8551e865525e27ac))

* ignore word2vec db &amp; vecs ([`32ee2c4`](https://github.com/tattle-made/feluda/commit/32ee2c429e0ab7d26914931ec6a9b9101a8ee18f))

* allow word2vec installation files ([`321b8e7`](https://github.com/tattle-made/feluda/commit/321b8e79dbafffeda0bb7609ee199ff716a34c73))

* debugging chore: create fresh indices on server start ([`947fd52`](https://github.com/tattle-made/feluda/commit/947fd5244fec4f8eb2da190816f181b9d08bae92))

* prettify logs&#39;
&#39; ([`32fbacb`](https://github.com/tattle-made/feluda/commit/32fbacb7f942ac0f420a1da423b6dc5d3f48529b))

* added error handling ([`1c598c5`](https://github.com/tattle-made/feluda/commit/1c598c5be545abf0b1392f49e4d877de57cfe49c))

* added error handling ([`224b44e`](https://github.com/tattle-made/feluda/commit/224b44e43ea1af5adac245dfe27dcd55044a4f1d))

* removed old code ([`c14325a`](https://github.com/tattle-made/feluda/commit/c14325aa9cf781d8e88c75a8a5722b2a2786c7c9))

* enabled indexing via singleton rabbitmq ([`8d3dd55`](https://github.com/tattle-made/feluda/commit/8d3dd555402a180d97472c94b3826628883cd23f))

* enabled indexing via singleton rabbitmq ([`28e1535`](https://github.com/tattle-made/feluda/commit/28e153535f7184d15b97854bda89ac3119a65913))

* copied api server side helper ([`e8e1a5d`](https://github.com/tattle-made/feluda/commit/e8e1a5d4b6b5ef1f61daa59ceaaed482e7c71215))

* add singleton es instance ([`e4d7215`](https://github.com/tattle-made/feluda/commit/e4d7215728b8937451f2944ef72042b8b6196214))

* enabled simple text search ([`4ecddb4`](https://github.com/tattle-made/feluda/commit/4ecddb40d7fa162b83cd77b588e382fe09340037))

* use wrapper func for indexing to avoid instantiating es here ([`e42692b`](https://github.com/tattle-made/feluda/commit/e42692b11ef08d88c5dbe744fdaf407b609ee0f4))

* return avg vid vec&#39;s index id &amp; define wrapper func for indexing ([`4d92228`](https://github.com/tattle-made/feluda/commit/4d9222874590fddd56166db1f88c72b85b6f2723))

* defined separate funcs for generatings vec ([`9615b59`](https://github.com/tattle-made/feluda/commit/9615b59d43512dfa79ff2e0389419f064115a1ca))

* import helper funcs for generating vecs ([`70e8c67`](https://github.com/tattle-made/feluda/commit/70e8c67aae68806bd82782363044b61cc18ddaf9))

* enabled image &amp; video search ([`e996e9b`](https://github.com/tattle-made/feluda/commit/e996e9b12d06f867f6cfa8edecc4d0d81ffa15e6))

* add combined_vec field for images ([`8377adc`](https://github.com/tattle-made/feluda/commit/8377adc47f34760cf33f3be9328f8570ca3e5ce4))

* helper for queue-less indexing ([`e34e201`](https://github.com/tattle-made/feluda/commit/e34e201009bdd47f8702551f428fe1bf1eccff48))

* update index fields ([`72071d6`](https://github.com/tattle-made/feluda/commit/72071d6ca3b8c6c7673a6e55e5fe48d99c9aac03))

* move import indexing code from helper ([`22bfef2`](https://github.com/tattle-made/feluda/commit/22bfef2e2bfd9e5a2251a61b5db11a6560bb01e3))

* enabled text vector based similarity search ([`87b7af1`](https://github.com/tattle-made/feluda/commit/87b7af1c7786f15ad7d027aeecb5ec1a1d104d40))

* removed unnecessary print statements ([`38fad38`](https://github.com/tattle-made/feluda/commit/38fad3840472b25f9af3e5a2cbd86498c7bcb837))

* enabled queue-less text indexing ([`e4758e9`](https://github.com/tattle-made/feluda/commit/e4758e9c43f4e1a3531c6be223874456ac7c946c))

* refactor ([`b76070b`](https://github.com/tattle-made/feluda/commit/b76070b71db36b9a7be023ca7caf8832cb8105a9))

* changed local ES host for development ([`b9f7ed3`](https://github.com/tattle-made/feluda/commit/b9f7ed3c847570bfcccaf4ead6bb2da309c189ce))

* renamed ([`9b664e3`](https://github.com/tattle-made/feluda/commit/9b664e32e1dfa372506df8afc77560b0916b03db))

* renamed ([`e7aec50`](https://github.com/tattle-made/feluda/commit/e7aec50aa97d3d9ae6f2ce266d09280127e8b125))

* moved index check/creation to server ([`bb39768`](https://github.com/tattle-made/feluda/commit/bb39768c122ce2db045577bce3a25747293cad68))

* helper for creating the indices ([`0c856a5`](https://github.com/tattle-made/feluda/commit/0c856a541e74f7b67b291cc60eb6124fe0f108f8))

* check if index exists on server start ([`092b264`](https://github.com/tattle-made/feluda/commit/092b264af643d7b17990d193f920fee6313ec3b0))

* fixed mongo local host ([`4a34440`](https://github.com/tattle-made/feluda/commit/4a344407235ccdfdd61c9a84ded8029418944863))

* add fields to mappings &amp; ensure text vecs are searchable ([`db37c20`](https://github.com/tattle-made/feluda/commit/db37c204f2c7b07ae688f47fd708af0d994d6dbe))

* explicitly specify which text analyzer ([`e9a6637`](https://github.com/tattle-made/feluda/commit/e9a66372eaaa984a73a30370fa93d383362ba570))

* ensure index with proper mapping exists before indexing ([`0cb9c85`](https://github.com/tattle-made/feluda/commit/0cb9c85df269ba228dcaeba852604516d46b7621))

* index text vec in elasticsearch ([`6158cf4`](https://github.com/tattle-made/feluda/commit/6158cf42065c6f53f44004e9050051bd4ec49848))

* (feat) add CD github action for development branch ([`a7236f4`](https://github.com/tattle-made/feluda/commit/a7236f4470e1f0987afc4b7019b71ca705fa6f32))

* Merge changes to elasticsearch host ([`35f0726`](https://github.com/tattle-made/feluda/commit/35f072605d5c1ee047d3830a58ecf631eaa3913d))

* (chore) wip ([`6504f59`](https://github.com/tattle-made/feluda/commit/6504f5993e6c8b1cdd75d52ea73abd264a8f4ea2))

* removed ([`78955df`](https://github.com/tattle-made/feluda/commit/78955df28c457596df1454677a3b92db26f1f62f))

* ignore docker logs, allow word2vec installation files ([`ba34c2e`](https://github.com/tattle-made/feluda/commit/ba34c2eb24b30420a0dc7394ddbb373aa7233e5b))

* update word2vec path ([`ebad682`](https://github.com/tattle-made/feluda/commit/ebad6824c66abcf210ba412f0b37fc3463a14df3))

* update word2vec path ([`ed44081`](https://github.com/tattle-made/feluda/commit/ed440818a5cce147a0550dc990e96ad849a2f91c))

* set up only word2vec.db &amp; include currently scraped langs ([`b8d826c`](https://github.com/tattle-made/feluda/commit/b8d826c61fa58168001128f8627dfa500fee20d2))

* word2vec &amp; alignedvec db setup scripts ([`73955a0`](https://github.com/tattle-made/feluda/commit/73955a04e691b1ad43669d516c9993b89abc361a))

* pass mongo db, collection names as env variables ([`d9a3ccd`](https://github.com/tattle-made/feluda/commit/d9a3ccd72755cd55cdb9da0efda7be262d953cc0))

* ignore google creds ([`282de50`](https://github.com/tattle-made/feluda/commit/282de504ace7d3b80a7662ecfe0ef5bb9e2c35b5))

* add creds for s3 bucket containing google application creds ([`22c75a5`](https://github.com/tattle-made/feluda/commit/22c75a511140bcb40e3ef5175f7608f2d38006b3))

* enable restart when receive.py is modified ([`cda7fdd`](https://github.com/tattle-made/feluda/commit/cda7fddc8124372cfbfae9399469972bfd107218))

* reduced batch size &amp; refactored ([`234ffab`](https://github.com/tattle-made/feluda/commit/234ffab62a7abc9ed603c7f08c625af351f2396e))

* refactored ([`f3aea6b`](https://github.com/tattle-made/feluda/commit/f3aea6b9832219e1402d0785e89ff4d5a22e720f))

* download google creds from s3 ([`92a0f34`](https://github.com/tattle-made/feluda/commit/92a0f34081e02b76e5718aadcfb4a6f3e2f911d0))

* added boto3 ([`bebb6a2`](https://github.com/tattle-made/feluda/commit/bebb6a2bbd7a0c0923b29782f34a2ec818832a5d))

* hstack instead of vstack with small batch sizes ([`ed02b10`](https://github.com/tattle-made/feluda/commit/ed02b1007a7f2c148bfcfd0f4572f3416dfa30d9))

* revert to original batchsize ([`cb0e9bf`](https://github.com/tattle-made/feluda/commit/cb0e9bfe33589bb038277015d3b1402d039c7991))

* try with batchsize=1 ([`4338661`](https://github.com/tattle-made/feluda/commit/4338661bc5cef807509334fe60c3f906a62727f6))

* updated .env instructions ([`c9276a1`](https://github.com/tattle-made/feluda/commit/c9276a1a81fcffe760ed4002229f4667c5f5c0a9))

* fixed formatting ([`27d43b1`](https://github.com/tattle-made/feluda/commit/27d43b1b5a22ec221c5488b876c0c4fe1c703be6))

* updated ([`a703fb9`](https://github.com/tattle-made/feluda/commit/a703fb939519486156ad8725914f5fb8dc482c5f))

* templates for env files ([`a6aa9a3`](https://github.com/tattle-made/feluda/commit/a6aa9a3ea4c55a00af8bea4124b834a58e82df21))

* don&#39;t import langdetect ([`deb28e7`](https://github.com/tattle-made/feluda/commit/deb28e72d3aa947975d215eee26b4993640f146b))

* time execution ([`b6fb235`](https://github.com/tattle-made/feluda/commit/b6fb23539e2ed11b360627d06d2c72be988c0fd6))

* pre-compiled requirements for copying in dockerfile ([`e1c8aa1`](https://github.com/tattle-made/feluda/commit/e1c8aa14eef3183660ea1b09cf6da18a13cb4fbb))

* add ffmpy, remove unused packages ([`9386cb4`](https://github.com/tattle-made/feluda/commit/9386cb4143a7660ee01c6ae3e78aab495fd7d30b))

* enable multistage builds &amp; leaner images ([`274805e`](https://github.com/tattle-made/feluda/commit/274805ede1d90ace66622eff5cd065872723119d))

* enable multistage build &amp; increase shared memory ([`9413527`](https://github.com/tattle-made/feluda/commit/9413527c7830ee30330a5a9889f832c480351264))

* increased heartbeat interval &amp; added publisher confirms ([`f5e215d`](https://github.com/tattle-made/feluda/commit/f5e215d6365436dc080c27575bfbb4a9f2b61df3))

* enable video compression with ffmpy ([`4deb006`](https://github.com/tattle-made/feluda/commit/4deb00671f43a31e39ac9effa26c107da1407ec4))

* return mongo id after indexing ([`88af964`](https://github.com/tattle-made/feluda/commit/88af96416bdd490ce3bfaba0d50ccaaf70b5ea96))

* allow queue-less indexing via original endpoints ([`d667e4a`](https://github.com/tattle-made/feluda/commit/d667e4a4bfab364f1e7f7a78ee69d9d1f755037e))

* added queueing, updated requirements, refactored code ([`49d5f51`](https://github.com/tattle-made/feluda/commit/49d5f51cde9edb5fd3a6483beddd573197f6f105))

* compute time taken ([`126b952`](https://github.com/tattle-made/feluda/commit/126b952e69247ded7fa9b9873ae331bcddb22b08))

* downloads &amp; unzips wordvecs with error handling ([`3417361`](https://github.com/tattle-made/feluda/commit/3417361f9d95578af456a905a603eaee1051fbd8))

* added wget ([`2dc98f3`](https://github.com/tattle-made/feluda/commit/2dc98f3de34480c02e44013095236c8a5affab5a))

* create single endpoint for all media uploads
index videos via file urls
make request data keys consistent with simple search ([`c28a342`](https://github.com/tattle-made/feluda/commit/c28a3425bc30f292cc40000318a2c14eaf21f179))

* Merge branch &#39;feature/dockerization&#39; ([`ad31800`](https://github.com/tattle-made/feluda/commit/ad31800684b4bc0b06cf2e03c17621d240963936))

* cherry picked changes from master ([`37b1584`](https://github.com/tattle-made/feluda/commit/37b1584515b8e0c79eece68ee8a295877d0532a1))

* added debugging statements ([`475b36e`](https://github.com/tattle-made/feluda/commit/475b36e6044975381d5b04481df777c3792b6723))

* sample cli commands for elasticsearch ([`555a10b`](https://github.com/tattle-made/feluda/commit/555a10b0b2f5201a5878fbe8ca3516c501f59d91))

* fixes, new generator for bulkdata upload for vidsearch index ([`9129f87`](https://github.com/tattle-made/feluda/commit/9129f87a44ee7ac32e506873093e6fd8cd1b8963))

* Merge branch &#39;master&#39; of github.com:tattle-made/tattle-api ([`4ef99b5`](https://github.com/tattle-made/feluda/commit/4ef99b5f1cf941b34fa9df9ec37fc6f16419fb9a))

* use new es video index ([`de9e2c5`](https://github.com/tattle-made/feluda/commit/de9e2c5aa6958e31bd56199f36a1b5722c3eff14))

* extract vid attrs, do sanity check ([`a2a1216`](https://github.com/tattle-made/feluda/commit/a2a1216f52b71a1a19a5f6e1025a3ac953b3ec0b))

* create_indices for vid, txt, img ([`9049ef0`](https://github.com/tattle-made/feluda/commit/9049ef0f57b1b606ac2591c8f6b0407cc51c7823))

* video search todo lis ([`a4092cf`](https://github.com/tattle-made/feluda/commit/a4092cff34abbf21d357cdcae678de3c20ef26b9))

* (fix) ([`99a7791`](https://github.com/tattle-made/feluda/commit/99a7791a33d3549ae52bc93818a70c755e8fd769))

* (feat) dockerize app ([`1a986cc`](https://github.com/tattle-made/feluda/commit/1a986cc4bf194a40fa07016c55367799026d4dba))

* streamlit app to testout word embeddings ([`4fdccc6`](https://github.com/tattle-made/feluda/commit/4fdccc610a46515625fd4ef1bd936a74ef3b5595))

* working upload_video, get mean_feature, upload to es ([`7a1e783`](https://github.com/tattle-made/feluda/commit/7a1e78310741bf437ae5b64c5766415ab3bebfa1))

* support passing vid as a param to run VideoAnlayzer as a script ([`0ecfb24`](https://github.com/tattle-made/feluda/commit/0ecfb24f622fb6143b67a243669063ed4f998ad6))

* don&#39;t overwrite feature_matrix while computing QR ([`57fc28c`](https://github.com/tattle-made/feluda/commit/57fc28c7181a5e827362ee91fe82e7fa3477a76d))

* VideoAnalyzer updates: extract features, find keyframes via QR ([`972e57a`](https://github.com/tattle-made/feluda/commit/972e57ad7570f1dd1b75a52c1e13c7e85e60d4df))

* updated es_test script ([`a26b210`](https://github.com/tattle-made/feluda/commit/a26b2104a75428a7fe7f6fad53854835d76df3eb))

* v0.1 upload_video api ([`53306a9`](https://github.com/tattle-made/feluda/commit/53306a982f9002632e98162b76f77ed9cdb3000b))

* VideoAnalyzer class ([`329fb5b`](https://github.com/tattle-made/feluda/commit/329fb5b29283bfbc9d228ace291fa5373b349973))

* Merge pull request #9 from tattle-made/dev/ngmuley/fix-install-for-mac

update install script for mac OS, update requirements.txt with latest… ([`3789a6b`](https://github.com/tattle-made/feluda/commit/3789a6b1b7c52127fffbc52b0406620bec406704))

* elastic search support, es_flag, and query_es method ([`17c8d6a`](https://github.com/tattle-made/feluda/commit/17c8d6adc767566401ef6adbc5d65aa685771348))

* setup local es on aws ([`fdd5198`](https://github.com/tattle-made/feluda/commit/fdd5198ae5cfa92144d470385b53ecb3e56775b7))

* Merge branch &#39;master&#39; of github.com:tattle-made/tattle-api ([`8f15776`](https://github.com/tattle-made/feluda/commit/8f15776e9d371e9cdf1a680a56b56f84d54e74a7))

* [fix] text len &lt; 3 error for detect_lang ([`3599d2c`](https://github.com/tattle-made/feluda/commit/3599d2cd2dfe23974a663325e46add59f67d1d33))

* es_test script ([`4b1a9df`](https://github.com/tattle-made/feluda/commit/4b1a9dffb361f3b50df9ff102d2eac56361196d3))

* update install script for mac OS, update requirements.txt with latest pip-compiled from requirements.in ([`6dfaa74`](https://github.com/tattle-made/feluda/commit/6dfaa745337381f74b6f99015d2c888e01a80618))

* db setup for aligned wordvecs ([`270220a`](https://github.com/tattle-made/feluda/commit/270220a6e413253401e097952cbdac5039461f88))

* return lang=None if text is empty ([`ae696d5`](https://github.com/tattle-made/feluda/commit/ae696d55e4f960a3eb73bcbee7f579cc6b60ec11))

* [fix] shorted uuid to fix mongodb 8-byte int issue ([`60f70f8`](https://github.com/tattle-made/feluda/commit/60f70f83f0da10aaf045e34cb89ff0048635e645))

* remove monitoring ([`c201313`](https://github.com/tattle-made/feluda/commit/c20131371ca1408afdc57c2a5f4ca3b116dfe9fd))

* only fetch top 10 docs from mongo ([`9113bbe`](https://github.com/tattle-made/feluda/commit/9113bbee799bbc2518e7167cd1cc9eeb7a54de00))

* Merge branch &#39;master&#39; of github.com:tattle-made/tattle-api ([`12b632d`](https://github.com/tattle-made/feluda/commit/12b632dc7fdae1f97dd91a9685e801c72f0cb9ba))

* monitor running time for a few functions ([`f638aa4`](https://github.com/tattle-made/feluda/commit/f638aa42839d2ad525966ec99999777041e974bb))

* monitor -&gt; timeit decorator ([`f393141`](https://github.com/tattle-made/feluda/commit/f3931411dea909b5784b5b84a847a7bba4006529))

* Merge pull request #7 from dennyabrain/feature/public-docs

(chore) add contributing and CoC readmes ([`892bc81`](https://github.com/tattle-made/feluda/commit/892bc816bdc09f137e8b04464bfa6fffce569bdf))

* (chore) add contributing and CoC readmes ([`d247215`](https://github.com/tattle-made/feluda/commit/d24721597c71a11709a192d191d2944ee416be9a))

* fix the missing words in word2vec db bug ([`75d74be`](https://github.com/tattle-made/feluda/commit/75d74be37b2aecc55f1625a18aad303c710d9978))

* limit duplicate docs at 10 ([`aa8b29a`](https://github.com/tattle-made/feluda/commit/aa8b29ab3bdc2b2ee763915bf06fa24f28142497))

* user textblob lib to detect language ([`0340cbd`](https://github.com/tattle-made/feluda/commit/0340cbd5eb528cd24c7a5871f894bcaea2f8066b))

* fix order of source issue in find_duplicate ([`04ce18e`](https://github.com/tattle-made/feluda/commit/04ce18e51ba51bd5cb5b49609f2de48748796ffb))

* return list of docs in order of match in find_duplicates ([`94ec663`](https://github.com/tattle-made/feluda/commit/94ec6633c1ab7543e524b3c95994bb9e80bd2791))

* default doc_id int instead of string ([`c38dc41`](https://github.com/tattle-made/feluda/commit/c38dc415a90644a4299d83fb4210d15baf4d2166))

* source for each doc, default tattle-admin ([`b39f7d7`](https://github.com/tattle-made/feluda/commit/b39f7d7d6865d76058d5bd81077a42665af7fed4))

* search_tags API, pass list of tags, list of sources ([`ac2c7a1`](https://github.com/tattle-made/feluda/commit/ac2c7a1c88b78986436036c4956bcebab1e3f3cf))

* support for flexible threshold passing in find_duplicate API ([`7e4f1f5`](https://github.com/tattle-made/feluda/commit/7e4f1f522106b1a1a405a4badaa92dfb97d7f092))

* remove_tags API and support for source in tags ([`a9f3568`](https://github.com/tattle-made/feluda/commit/a9f356852a327bd75808f272cce9cf80d5d28ebf))

* delete_doc API ([`0074efc`](https://github.com/tattle-made/feluda/commit/0074efc0fb7961bc161c185edfb8efd580ba36b0))

* ebextension packages ([`8ce9655`](https://github.com/tattle-made/feluda/commit/8ce9655a5cfa2ade3eeebd55d421584f768d9848))

* torch to requirements ([`f341f13`](https://github.com/tattle-made/feluda/commit/f341f13f645ca4630a28d9b84be8c57f92f5fea7))

* remove torch stuff from requirements, to be installed separately ([`58f06e9`](https://github.com/tattle-made/feluda/commit/58f06e9127ba8109a6624961edb8217090a45bb8))

* video analysis notebook changes ([`0d649e0`](https://github.com/tattle-made/feluda/commit/0d649e0dbc006399ff80e607868516e446133e84))

* word2vec script change ([`c905ebd`](https://github.com/tattle-made/feluda/commit/c905ebd0f46204a207ce3f87bfcbe2d7078c4b12))

* eb config ([`bf6c156`](https://github.com/tattle-made/feluda/commit/bf6c1565e5f8275b6b361664990b4ca8451cf9a7))

* fix, docsearch -&gt; textsearch ([`f615d79`](https://github.com/tattle-made/feluda/commit/f615d79196cbee10c3c3188d356fc2e9121c0be9))

* remove single quotes to avoid messing up the sql query ([`0b99cbf`](https://github.com/tattle-made/feluda/commit/0b99cbf3eeaa051be1367cc910cb29bd0d87be89))

* handle en,gu,hi language ids ([`1f83db6`](https://github.com/tattle-made/feluda/commit/1f83db634bdf6615fc47703268849528fcce77b8))

* fix another png issue ([`3b7170c`](https://github.com/tattle-made/feluda/commit/3b7170c7a627e3bbc3afe4b59e149e29d0ab7789))

* separate image search, text search, doc search(text+image) ([`274d3e1`](https://github.com/tattle-made/feluda/commit/274d3e1ca70ee9bd35f4b15d80b79e0c0d3fd4f4))

* take care of new lines in text ([`644fad0`](https://github.com/tattle-made/feluda/commit/644fad05a2fe01dc59a3b9e5b4ea0c6fb4fbc16e))

* closes #2, convert RGBA to RGB ([`089a049`](https://github.com/tattle-made/feluda/commit/089a04913b806453be02aebe908c1109bc10548b))

* error checking for detect_text ([`d958744`](https://github.com/tattle-made/feluda/commit/d9587445a980d5241f359f641c4314fa0805dbe9))

* find_text API end point for finding text inside images ([`382c086`](https://github.com/tattle-made/feluda/commit/382c0863d6942facabbb9977128836a97ab5f2f1))

* fix detect_text function ([`86e3cbf`](https://github.com/tattle-made/feluda/commit/86e3cbfbaadf8e05db0ad39f58d4e257c771dd93))

* Merge branch &#39;master&#39; of github.com:tattle-made/tattle-api ([`1806859`](https://github.com/tattle-made/feluda/commit/1806859befd8cca1d526f4650b5b786a7c94490b))

* video analysis experiments ([`e5d398f`](https://github.com/tattle-made/feluda/commit/e5d398f5acf408e495bd1eed7bde01ca41156a5d))

* support for searching document vectors ([`c0f07f8`](https://github.com/tattle-made/feluda/commit/c0f07f849484c25cdf05ce007a26054fdf1c8f3b))

* search threshold to 0.6, handle None vec ([`1d0fe7b`](https://github.com/tattle-made/feluda/commit/1d0fe7bdd8ef121d3a0c6ad0f7d04e0bb26890c4))

* doc vectors search support ([`0350d69`](https://github.com/tattle-made/feluda/commit/0350d697730b44805b4b505c44f66f2610abc24f))

* [fix] imports ([`099988e`](https://github.com/tattle-made/feluda/commit/099988effec9b401bc5bd62680b6687f20c71b43))

* [fix] import requests ([`c9bc592`](https://github.com/tattle-made/feluda/commit/c9bc592c617d3b76bbabd4d67070a9cddd14cd21))

* full index on wordvecs ([`6215c3b`](https://github.com/tattle-made/feluda/commit/6215c3b2622485cbbf2e67d58e5ff88738385cc1))

* doc2vec method ([`95e9456`](https://github.com/tattle-made/feluda/commit/95e94561b5b3cd2d8da9bfbcd43e940d0c1a44ce))

* ignore .vec and .db files from git ([`1c48ecc`](https://github.com/tattle-made/feluda/commit/1c48eccc9a988da036db8c147f13b9788543c390))

* scripts to generate word2vec database ([`b288ddb`](https://github.com/tattle-made/feluda/commit/b288ddb6a5094ac1bdb4080b8d724133d50c33d9))

* install_torch script ([`0da5955`](https://github.com/tattle-made/feluda/commit/0da5955db3a52badfbb10b0e8cc8b39cde122178))

* detect_lang function ([`b82e1e8`](https://github.com/tattle-made/feluda/commit/b82e1e8032e17a87ddeb184df795440d0fd5a999))

* move image_from_url to analyzer ([`ca36f7d`](https://github.com/tattle-made/feluda/commit/ca36f7d6dc4afeccec709a726acce00d3fcb3c51))

* fasttext, langdetect depedencies ([`a29cb1d`](https://github.com/tattle-made/feluda/commit/a29cb1d5217b7aa0a1a1fd285c52557b2ff4926e))

* update_tags api ([`51e1ba4`](https://github.com/tattle-made/feluda/commit/51e1ba4e2bf49bc8248a7419f1cd59664074b12c))

* fix has_text field ([`c885ea4`](https://github.com/tattle-made/feluda/commit/c885ea4b8ae788939d3f80aad2a4c48d02f22048))

* tags field for documents ([`1ad64a8`](https://github.com/tattle-made/feluda/commit/1ad64a89b5d615594d61ace49af18136e633681a))

* update imagesearch when a new image is uploaded ([`0be7859`](https://github.com/tattle-made/feluda/commit/0be7859a0190feca4718206b4e31467879ea5aa1))

* support to search for images in find_duplicate ([`89347cb`](https://github.com/tattle-made/feluda/commit/89347cbae8e42b819b0b337ec2e88e1ce75ece64))

* add tqdm updated requirements.txt ([`6b994e8`](https://github.com/tattle-made/feluda/commit/6b994e808e3ff3e0113c76c9c249b03481695c2f))

* add image fingerprint with each upload_image call ([`ac7db71`](https://github.com/tattle-made/feluda/commit/ac7db718ecfebb9f2bbf1e320aee43df3ec8045b))

* support for doc_id for upload_text and upload_image apis ([`409d7f0`](https://github.com/tattle-made/feluda/commit/409d7f0a35ed44e060fa032bd613d7508ee05bc2))

* text detection in uploaded image ([`02c0d1f`](https://github.com/tattle-made/feluda/commit/02c0d1fc51555ef7f6a4d4ce407837fb70552188))

* fix image_upload api ([`bfd59e4`](https://github.com/tattle-made/feluda/commit/bfd59e4f159c68fbc8a6fc3cbe13b28357c7df78))

* some tests ([`489093f`](https://github.com/tattle-made/feluda/commit/489093f0ae88c31a4adecb096831e8b3e77cf644))

* upload_image api ([`67be7d8`](https://github.com/tattle-made/feluda/commit/67be7d808173bc7d09aa0ab2ab8c9a55f8d6f8cf))

* find_duplicate API, add support for text ([`13cce36`](https://github.com/tattle-made/feluda/commit/13cce36f4f8d9f501e861875871009b43a974198))

* upload_text API ([`d4dbbf2`](https://github.com/tattle-made/feluda/commit/d4dbbf2523a1c6eb7f212b0cffccbeb36742d7c0))

* ignore etc, share ([`e698a2a`](https://github.com/tattle-made/feluda/commit/e698a2aa9f2dea65b63b78b19a256a7caf8999ec))

* dnspython requirement ([`249875c`](https://github.com/tattle-made/feluda/commit/249875cdaad9e85372fff5966a09c811367ee344))

* test for text docs ([`96269a5`](https://github.com/tattle-made/feluda/commit/96269a55f4dcb905199112b6321c2c169dec50b0))

* pymongo requirement ([`a099621`](https://github.com/tattle-made/feluda/commit/a099621db56f5076af0d8bfb66025267fbac100e))

* application loop ([`1691203`](https://github.com/tattle-made/feluda/commit/16912030cd061cf4d2a4264aff5783c5aa5f7806))

* fix Dockerfile pip install ([`5d6c87b`](https://github.com/tattle-made/feluda/commit/5d6c87b80f1bd28dba460eb058cc49586c272df1))

* try to fix Dockerfile ([`9d67658`](https://github.com/tattle-made/feluda/commit/9d676584bd39e0b4e674776d6453bd9af5ed87f9))

* requirements.txt, to avoid installing pip-tools on server ([`2f744a0`](https://github.com/tattle-made/feluda/commit/2f744a09f2e5d952bc78d2d5672ebf5bf979dd55))

* ignore eb files ([`c9df037`](https://github.com/tattle-made/feluda/commit/c9df0373a69887545c3c398f256e0307751bb8c5))

* add dockerfile ([`09919f7`](https://github.com/tattle-made/feluda/commit/09919f72be47abb6c4d139848d6d01518699118f))

* torch, skimage dependencies ([`a4bf37e`](https://github.com/tattle-made/feluda/commit/a4bf37e046b21432d8c2bc5256f031e380fa326a))

* api name change ([`0eb9df7`](https://github.com/tattle-made/feluda/commit/0eb9df78b1d5728e986ce9b031547208883df796))

* tests ([`181127a`](https://github.com/tattle-made/feluda/commit/181127a0c8965d35442d21b711f3ed581ca39824))

* feature extraction for images ([`3987959`](https://github.com/tattle-made/feluda/commit/3987959b2bc4e69a75106176696caa5a73f547e4))

* format readme ([`b6fc431`](https://github.com/tattle-made/feluda/commit/b6fc431eb94faf7d6e904d17b562c5d1771e0ce7))

* ignore data dir ([`09f2210`](https://github.com/tattle-made/feluda/commit/09f22106bf554eef0df171f285b105213da83ad0))

* analyze.py, try google vision api ([`5ec1e03`](https://github.com/tattle-made/feluda/commit/5ec1e0356ba331ad764e98d2ee09f3b67735f033))

* gitignore ([`320b19b`](https://github.com/tattle-made/feluda/commit/320b19b2cdc26891acfc34d13c576048b93c422c))

* init ([`ca74ede`](https://github.com/tattle-made/feluda/commit/ca74edea0e2779ef506eb0f69fb53010b1daba02))
