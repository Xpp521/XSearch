## v1.3.0.a1
#### Features
- Test translation function, switch keyword: "fy". Currently there is only one provider: YouDao (only available in mainland China).

#### Refactor
- Optimize newVersionChecker logic.

## v1.2.2
#### Bug Fixes
- Fix text display incompleteness;
- Fix newVersionChecker always returns False;
- Fix settingDialog's logo font display error on some devices.

#### Refactor
- Get rid of "lxml" module;
- Reduce application package size;
- Add "Resources" module, move all resources (image、ttf...) to it.

## v1.2.1
#### Bug Fixes
- Fix suggestion list appears delay just after switching suggestion providers.

#### Refactor
- Optimize new version check logic;
- Restructure SuggestionGetter module. 

## v1.2.0
#### Features
- Add a new suggestion provider: Google.
#### Refactor
- Restructure and rename "Strings" module to "Languages";
- SuggestionGetter and NewVersionChecker now share the same background thread;
- Rewrite README.md and add Chinese version.

## v1.1.0
#### Features
- Add check update;
- Add open source address and author message.
#### Refactor
- Optimize Strings module;
- Adjust SuggestionGetter module.

## v1.0.0
- The first stable version.

## v0.0.2
#### Features
- Add GPL license.
- Add icons for tray icon menu.
#### Bug Fixes
- List view: fix the list view of search dialog does not disappear when keyword is empty.
- Search engine icon: fix the search engine icon does not change with search engine.
#### Refactor
- Optimize SuggestionGetter module.

## v0.0.1
- The first version.
- Setting dialog progress: 80%.