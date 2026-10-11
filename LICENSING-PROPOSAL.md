# PaNasMs licensing proposal

**Draft for review — not an operative license or additional permission.**

The existing LICENSE and NOTICE remain in effect. This document does not relicense
any code, published package, third-party component or hardware design. The proposed
terms below need legal review before adoption, particularly the hardware-sale and
service exceptions. Git authorship alone does not establish relicensing rights.

## Owner's intended policy

- Allow personal use and internal business use, without a company-size limit.
- Allow modifications and free redistribution, including forks.
- Allow charging for installation, configuration, maintenance and technical support
  on equipment already owned by the customer.
- Do not allow selling the software or derivative versions, or including them in any larger product sold to a customer, without a separate
  written agreement with the applicable rights holders.
- Require distributed versions to credit the original project and retain its URL.
- Do not require publication of modifications merely because they were made.

## Basis and identity

Use the complete [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
as the base, subject to the restrictions below. The restriction structure is
inspired by [Commons Clause 1.0](https://commonsclause.com/), but its definition of
selling is deliberately replaced to match this project's policy. Standard Commons
Clause includes certain services and a substantial-value test that does not
unambiguously exclude every commercial hardware bundle.

Proposed name: **PaNasMs Source-Available License 1.0**.

This is a custom combined license, not unmodified Apache 2.0, not standard Commons
Clause, and not an OSI-approved open-source license. Apache 2.0 must not be offered
as an independent alternative for the covered software. Package metadata must not
identify the combined license as `Apache-2.0` alone.

## Proposed supplemental terms

The following is the draft normative text. It would accompany the complete Apache
License 2.0 in a single operative LICENSE upon adoption, not replace its full text
with a URL or put binding restrictions solely in an informational NOTICE.

### 1. Scope and priority

"Software" means original PaNasMs material expressly distributed under these
combined terms, in source or object form, including covered portions incorporated
into Derivative Works as defined by Apache License 2.0. "Licensor" means the
applicable copyright owner or an entity authorized by that owner.

The permissions in Apache License 2.0 are subject to these supplemental terms.
Where they conflict, these supplemental terms control. No permission is granted
by these combined terms to perform an act prohibited below. Prior written approval and a separate written agreement with the applicable
rights holders are required to authorize otherwise prohibited activities. An
acknowledgment, informal discussion or attribution alone is not such an agreement.

These terms do not change the licenses of separately identified third-party
material or claim rights over independent software merely communicating with the
Software. They do not limit rights that applicable law gives independently of this
license.

### 2. Permitted use and redistribution

You may use and modify the Software for personal purposes and your organization's
internal business operations. You may redistribute it, including Derivative
Works, without charging for the Software and subject to sections 3–5 below and
the requirements of Apache License 2.0.

There is no obligation under these combined terms to publish source code for
private modifications or to distribute source code instead of object code.
These terms must accompany all distributed copies containing the Software;
downstream terms must not remove these restrictions from the covered material.

### 3. Prohibited sales and commercial product bundles

Without prior written approval and a separate written agreement with the applicable
rights holders, you may not:

1. Sell or license copies of the Software for a fee or other consideration,
   including covered copies within renamed, modified or derivative versions.
2. Incorporate, embed, bundle or otherwise supply the Software as part of any
   larger product sold or licensed for a fee or other consideration, whether that
   product is hardware, software, an appliance, a virtual-machine image or a
   container image. This applies even if the product adds substantial independent
   functionality or the Software itself is described as free.
3. Supply hardware for sale with the Software installed, preloaded on included
   storage media, or otherwise included as part of the hardware transaction.
   This includes new and used NAS devices and other computers.
4. Arrange installation or delivery of the Software as an included or mandatory
   part of a hardware sale, including installation performed after transfer of
   ownership or through another party on the seller's behalf.

These restrictions apply regardless of whether the Software is separately priced,
advertised as free, bundled with other software, or accompanied by a charge
described as assembly, configuration or support. They apply without a test of how
much of the larger product's value comes from the Software.

Selling hardware without the Software does not violate these terms. A purchaser
may independently obtain and install the Software after buying that hardware.
A public link to the project's website alone does not constitute a hardware
bundle when no copy, installation or entitlement to installation is supplied as
part of the transaction.

### 4. Paid services on customer-owned equipment

You may charge for installation, configuration, maintenance, repairs, training
and technical support for the Software on equipment already owned by the customer.
You may make and install copies reasonably necessary to deliver those services,
including service-related modifications, provided that:

- The customer receives the Software under these combined terms and is not
  charged a software license, copy or access fee.
- The service is independently obtained for customer-owned equipment, rather
  than included in, required by, or arranged as part of the equipment's sale.
- The product-sale and hardware-bundle prohibitions in section 3 is not circumvented by splitting
  invoices, delaying installation or nominally transferring hardware ownership
  immediately before a bundled installation.
- You act on your own behalf, do not imply endorsement by PaNasMs, and comply
  with Apache License 2.0 section 9 when accepting support or warranty liability.

An ongoing support subscription is permitted on the same conditions. These
permissions do not make a prohibited hardware or software product bundle permissible.

### 5. Attribution and modifications

Every distributed copy containing the Software must retain a readable notice:

> Based on PaNasMs — Pavlo's NAS Management System, by Pavlo Matviienko and
> contributors. Original project: https://github.com/PaNasMs/panasms

Keep applicable copyright and third-party attribution notices. Include the
original-project notice in an accompanying NOTICE file, documentation, or a
normally accessible legal/about screen. A forced startup banner or permanent
logo is not required. Forks may use another name but must not imply that they are
official releases or endorsed by the original authors.

For distributed modifications, preserve the changed-file notices required by
Apache License 2.0 section 4(b). Attribution is not a transfer of ownership and
does not authorize use of the project's trademarks beyond identifying origin.

## Scenario checks

| Scenario | Intended result |
| --- | --- |
| Home user installs on their NAS | Allowed |
| Company installs on its own NAS to store business files | Allowed |
| Consultant installs and configures on a customer's existing NAS for a fee | Allowed |
| Monthly support for that NAS | Allowed |
| Free fork, with original attribution and change notices | Allowed |
| Selling an appliance, paid software suite or VM image containing PaNasMs, even as a free component | Prior approval and a separate written agreement required |
| Selling a renamed fork containing PaNasMs code | Prior approval and a separate written agreement required |
| Selling a NAS with "free PaNasMs included" | Prior approval and a separate written agreement required |
| Selling a NAS and including installation on a second invoice | Prior approval and a separate written agreement required |
| Private resale of a used NAS with PaNasMs still installed | Prior approval and a separate written agreement required under this draft; remove it before sale |
| Selling a blank NAS, followed by the buyer's independent self-installation | Allowed |
| Selling an independent application that only uses a public PaNasMs API | Not restricted solely by that API use |

## Review points before adoption

1. Confirm the used-hardware consequence above: the owner requested a hardware
   sales prohibition without a commercial-vendor-only exception.
2. Hosted NAS/storage services were not discussed. This proposal does not import
   Commons Clause's broad hosting prohibition. Do not promise a hosting ban without
   a separate policy decision and precise wording.
3. Review enforceability, statutory resale/exhaustion rules, definitions of paid
   access versus support, and contributor grants with a qualified licensing lawyer.
   This draft cannot guarantee a hardware-sale restriction in every jurisdiction.
4. Verify relicensing authority for each covered contribution and preserve all
   third-party exceptions. Copyright remains with each rights holder.

## Adoption checklist

- Review scope in panasms, backend, frontend, module-sdk, module-files,
  module-terminal, module-cloud-sync, module-containers, module-registry, updates,
  panasms-oauth-gateway and the project website. Do not relicense all files solely
  because they share a repository.
- Publish one identical complete combined license with an explicit version and
  consistent NOTICE attribution; preserve third-party notices.
- Update current package manifests, README references, website terms, installer
  notices and build packaging. Use an appropriate custom license identifier or
  `SEE LICENSE IN LICENSE` where supported; verify the module schema first.
- Do not rewrite license metadata in old signed catalogs, released packages,
  Git tags or existing releases. Previously granted rights remain governed by the
  terms under which those copies were obtained.
- Ensure new artifacts contain the complete license and notices before publication.
- Keep CAD/chassis, upstream CasaOS materials and other third-party assets outside
  this software license. Their rights require separate consideration.

No adoption or relicensing is performed by merging this proposal document.
