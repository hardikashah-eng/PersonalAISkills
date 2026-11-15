# Adding a photo of a good time together

Shared by ThankYou and Reconnect. A real photo from a moment the two of them
shared, such as the team at the launch, the hike, or the whiteboard from that
night, says "I remember" more than any sentence can. It is optional: when no
good photo exists, use a pencil sketch of the moment instead (`sketch.md`).
Record where the picture came from as `"source": "own"` in `note.json`.

## Non-negotiables

1. **Only the user's own photos.** Use photos from the user's own library or
   drive (Google Photos, OneDrive, iCloud or a local folder they connect),
   photos they attach in the chat, or photos the two people already sent each
   other (email attachments, chat images; WhatsApp and SMS only with the same
   opt-in as the messages). **Never** take photos from the web, from social
   media profiles, or from the recipient's own accounts, and never use a
   profile picture.
2. **Never identify people by their face.** Do not run face recognition or
   ask a search engine who someone is. Find candidate photos by context only:
   the date and place of the moment, the album or event name, the thread they
   were shared in, captions, or person labels the user already created in
   their own photo app. The user confirms who is in the photo.
3. **The user picks the photo.** Show 2–4 candidates (or describe them if
   thumbnails can't be shown) and use only the one they choose. If the user
   has doubts, skip the photo.
4. **Never alter a person.** Do not edit, retouch, beautify, age, swap, or
   generate faces or bodies, and never create a fake or AI-made "photo" of
   the people. Allowed edits: crop, straighten, resize, gentle overall
   brightness or contrast, and, when the user asks, turning the whole photo
   into a pencil sketch (`scripts/sketch_photo.py`, which restyles the entire
   image evenly and changes no one's features).
5. **Strip hidden data.** Remove EXIF and other metadata (GPS location, device
   serial, timestamps) before the photo goes into a card or draft.
   `scripts/render_card.py` does this automatically.
6. **Keep it private.** A card with a personal photo is for the recipient
   only. Deliver it as a file or a draft, and don't publish it as a public or
   shareable link unless the user explicitly asks. Don't copy photos anywhere
   else or keep them after the note is done.

## Finding candidates

Search narrow to wide and stop at a handful:

1. **Photos tied to the moment.** If the note is about the 2019 launch or the
   Austin offsite, look in that date range or album.
2. **Photos the two people exchanged.** Attachments in their email or chat
   threads are already shared between them, so they are the safest choice.
3. **Albums or person labels** the user made, such as "Team offsite 2019" or a
   person group the user named "Maya".
4. **Ask the user.** "Do you have a photo from that time together? You can
   attach it here." This is often the fastest route.

A photo doesn't need to show people. The whiteboard from that night, the two
chai glasses, or the trail where you hiked can be just as personal and avoids
many of the concerns below.

## Choosing: is this photo right for this person?

Use a photo only if every answer is yes:

- **Happy and kind.** Is it from a good time, and would they be glad to see
  it? Is it flattering to them, with no awkward expression and nothing they
  might be self-conscious about?
- **Appropriate for anyone to see.** It contains no alcohol-heavy party
  scenes, swimwear, or anything risqué, and nothing from a hospital, a
  funeral, or a hard time.
- **The right people.** It shows the two of them, or a group at a shared event
  that they both belonged to. Avoid photos where other people are the focus,
  and avoid other people's children. A child of either person appears only if
  the user chooses it and it fits the relationship (family, close friends).
- **No triggers.** It contains no former partner, no one the recipient has
  lost or is estranged from (unless the user specifically wants a remembrance),
  and nothing tied to a sensitive topic for them.
- **No giveaways.** No house numbers, street signs near a home, licence plates,
  badges, screens, documents, or anything confidential in the frame. Crop them
  out or pick another photo.
- **Culturally fitting.** Some people or communities prefer not to share
  photos of themselves, of women in the family, or of elders. When the culture
  makes this relevant and the user hasn't said, ask. Photos of someone who has
  passed away carry special weight in many traditions, so include them only at
  the user's explicit request.
- **Recent, but not surveillance.** For Reconnect especially, the photo must
  be from their *shared* past, never from the recipient's recent posts.

## Caption

One short line under the photo, warm and specific, with no personal details:
"The night the demo finally worked, 2019" or "Friday chai, launch week". A
city or event name is fine, but never a home, school, or workplace address.
The caption goes through `safety_check.py` like the rest of the note.

Alt text: a plain description for screen readers ("Two cups of chai on an
office table"). Never name anyone in the alt text unless the user wants it.

## Delivery

- **Card:** `render_card.py note.json --art art.svg --photo photo.jpg` puts
  the photo in a small instant-photo frame with the caption. It strips
  metadata and, if Pillow is installed, shrinks the photo to at most 1200 px.
- **Email draft:** attach or embed the stripped photo, never the original file.
- **WhatsApp or SMS:** suggest sending the photo first, then the message. A
  photo with "Found this today and smiled" is one of the warmest openers there
  is. Give the user the stripped copy to send.
