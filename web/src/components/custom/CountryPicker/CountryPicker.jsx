import { COUNTRIES } from "./countries";
import React, { useState } from 'react'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

const FlagIcon = ({ countryCode }) => (
  <img
    src={`https://purecatamphetamine.github.io/country-flag-icons/3x2/${countryCode}.svg`}
    alt={`Flag of ${countryCode}`}
    className="inline mr-2 h-4 w-6 rounded-sm object-cover"
  />
)

export default function CountrySelect() {
    const [selectedCountry, setSelectedCountry] = useState("")
  
    return (
      <Select onValueChange={setSelectedCountry} value={selectedCountry}>
        <SelectTrigger className="w-[300px]">
          <SelectValue placeholder="Select a country">
            {selectedCountry && (
              <>
                <FlagIcon countryCode={selectedCountry} />
                {COUNTRIES.find(country => country.value === selectedCountry)?.title}
              </>
            )}
          </SelectValue>
        </SelectTrigger>
        <SelectContent>
          {COUNTRIES.map((country) => (
            <SelectItem key={country.value} value={country.value}>
              <FlagIcon countryCode={country.value} />
              {country.title}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    )
  }
