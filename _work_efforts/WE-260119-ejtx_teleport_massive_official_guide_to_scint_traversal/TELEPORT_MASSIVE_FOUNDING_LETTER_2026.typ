#import "@preview/letterloom:1.0.0": *

#show: letterloom.with(
  // Sender's contact information
  from-name: "Justin Ross",
  from-address: [
    Teleport Massive (Pre-Incorporation)
    \
    San Francisco, California
    \
    #raw("justin.ross@teleportmassive.com")
  ],

  // Recipient's contact information (generic for case file)
  to-name: "Prospective Founding Team Members & Investors",
  to-address: [
    Deep Tech Community
    \
    San Francisco Bay Area
  ],

  // Letter date
  date: datetime(year: 2026, month: 1, day: 15).display("[day padding:zero] [month repr:long] [year repr:full]"),

  // Opening greeting
  salutation: "Dear Prospective Founders and Investors,",

  // Letter subject line
  subject: text(weight: "bold")[#smallcaps("Founding Opportunity: Scaling Quantum Teleportation from Mini to Macro")],

  // Closing phrase
  closing: "Sincerely yours,",

  // Signature
  signatures: (
    (
      name: "Justin Ross",
      title: "Founder & Vision Lead",
      affiliation: "Teleport Massive (Pre-Incorporation)",
    ),
  ),
)

// Letter content
I am writing to you today because I believe we stand at a pivotal moment in human history. Recent breakthroughs in quantum teleportation research have demonstrated something remarkable: quantum entanglement can be scaled. We've seen teleportation between distant superconducting chips over 64-meter distances, teleportation coexisting with classical communications over 30-kilometer fiber links, and teleportation over thermal microwave networks. The physics is clear—we can teleport bigger and bigger things safely.

#v(0.5cm)

I am assembling a founding team to establish Teleport Massive Inc., a company dedicated to systematically scaling quantum teleportation from laboratory demonstrations to real-world applications. Our mission is to push the boundaries of what can be teleported: from particles to atoms, from atoms to molecules, from molecules to chips, and ultimately to macroscopic objects—all while maintaining the highest standards of safety and fidelity.

#v(0.5cm)

The research foundation is solid. Seven peer-reviewed papers, compiled in the accompanying document, demonstrate a clear trajectory: teleportation is scaling up—from particles to chips, from short distances to kilometers, from ideal conditions to real-world environments. We are at the "chips" stage today (64m teleportation, 78.3% fidelity). Our vision is to systematically push these boundaries further, making distance irrelevant for all of humanity.

#v(0.5cm)

We are seeking founding team members who share this vision and can help us get this off the ground. We need quantum physicists and engineers who understand entanglement scaling, business and operations leaders who can build the infrastructure, legal and compliance experts who can navigate the regulatory landscape, and marketing strategists who can communicate this transformative technology to the world.

#v(0.5cm)

We are also seeking seed funding to establish our research infrastructure, validate our protocols at current state-of-the-art scales, and begin the systematic scaling process. This is a long-term vision—we're planning for an 86-year journey that will ultimately lead to technologies we can only begin to imagine today.

#v(0.5cm)

The enclosed documents provide the complete scientific foundation for our vision, our proposed mission and values, and detailed research findings. I invite you to review these materials and consider joining us in this endeavor. Together, we can build the future of transportation, communication, and human connectivity.

#v(0.5cm)

I look forward to discussing this opportunity with you further.

Thank you for your consideration.
