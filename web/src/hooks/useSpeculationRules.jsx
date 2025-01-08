import { useEffect } from "react";

const useSpeculationRules = () => {
  useEffect(() => {
    // Find all anchor links on the page

    // Generate speculation rules JSON
    const speculationRules = {
      prerender: [
        {
          source: "list",
          urls: [
            "https://vat.berlin-united.com//data/1/image/1",
            "https://vat.berlin-united.com//data/1/image/2",
            "https://vat.berlin-united.com//data/1/image/3",
            "https://logs.berlin-united.com/2024-07-15_RC24/2024-07-15_20-00-00_BerlinUnited_vs_SPQR_half1-test/extracted/2_16_Nao0017_240715-1830/log_bottom/0005623.png",
            "https://logs.berlin-united.com/2024-07-15_RC24/2024-07-15_20-00-00_BerlinUnited_vs_SPQR_half1-test/extracted/2_16_Nao0017_240715-1830/log_bottom/0007601.png",
          ],
        },
      ],
    };

    // Inject the speculation rules script
    const script = document.createElement("script");
    script.type = "speculationrules";
    script.dataset.speculationrules = true;
    script.textContent = JSON.stringify(speculationRules);

    // Append to head
    document.head.appendChild(script);

    // Cleanup on unmount
    return () => {
      document.head.removeChild(script);
    };
  }, []);
};

const useSpeculationRulesOld = () => {
  useEffect(() => {
    // Find all anchor links on the page
    const links = Array.from(document.querySelectorAll("a[href]"))
      .map((link) => link.href)
      .filter((href) => href.startsWith(window.location.origin)); // Filter for same-origin links

    // Generate speculation rules JSON
    const speculationRules = {
      prerender: links.map((href) => ({ source: "list", urls: [href] })),
    };

    // Inject the speculation rules script
    const script = document.createElement("script");
    script.type = "speculationrules";
    script.dataset.speculationrules = true;
    script.textContent = JSON.stringify(speculationRules);

    // Append to head
    document.head.appendChild(script);

    // Cleanup on unmount
    return () => {
      document.head.removeChild(script);
    };
  }, []);
};

export default useSpeculationRules;
