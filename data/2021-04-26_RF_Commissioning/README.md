# 2021-04-26 - TWA mockup RF Tests

| Time | Pin/duration | fMhz | Comment | 
| :--: | :----------: | :--: | :-----: |
| 07-45-11 | 200 kW / 0.2s | 55.5 MHz | test: oscillation on the power |
| 07-49-30 | 500 kW / 0.2s | 55.5 MHz | oscillations  |
| 07-55-25 | 500 kW / 1s | 55.5 MHz |   |
| 08-01-58 | 500 kW / 1s | 55.5 MHz | 1s double - arcs again  |
| 08-04-35 | 500 kW / 1s | 55.5 MHz | arcs  |
| 08-32-39 | 500 kW / 1s | 55.5 MHz | monitoring Pr on charge, antenna and gen (oscilloscope)  arcs |
| 09-06-46 | 600 kW / 1s | 55.5 MHz | monitoring Pr on charge, antenna and gen (oscilloscope)  arcs |
| 09-56-09 | ? | 55.5 MHz | ? |
| 11-10-22 | 400 kW | 55.5 MHz | OK |
| 11-11-47 | 500 kW | 55.5 MHz | OK |
| 11-11-57 | 600 kW | 55.5 MHz | SHAD triggers |
| 11-21-24 | 600 kW | 55.5 MHz | repeat without SHAD -> OK | 
| 11-21-59 | 600 kW | 55.5 MHz | repeat without SHAD -> OK | 
| 11-31-08 | 700 kW | 55.5 MHz | repeat without SHAD -> OK |
| 11-31-08 | 800 kW | 55.5 MHz | repeat without SHAD -> OK |
| 11-31-08 | 900 kW | 55.5 MHz | repeat without SHAD -> OK |
| 11-31-08 | 900 kW | 55.5 MHz | repeat without SHAD -> OK |
| 11-33-46 | 1000 kW | 55.5 MHz | repeat without SHAD -> OK |
| 11-34-19 | 1000 kW | 55.5 MHz | repeat with SHAD -> SHAD triggers |
| 11-37-38 | 1000 kW | 55.5 MHz | repeat with SHAD -> SHAD triggers |
| 11-38-11 | 1000 kW | 55.5 MHz | repeat without SHAD -> OK |
| 11-47-36 | 100 kW | 46.0 MHz | repeat without SHAD with Pr/Pi set to 0.650 at 46 MHz to create Pr -> OK |
| 11-50-34 | 100 kW | 46.0 MHz | repeat without SHAD with Pr/Pi set to 0.200 at 46 MHz to create Pr -> trigger |
| 11-51-13 | 100 kW | 46.0 MHz | repeat without SHAD with Pr/Pi set to 0.500 at 46 MHz to create Pr -> OK  |
| 11-51-56 | 100 kW | 46.0 MHz | repeat without SHAD with Pr/Pi set to 0.400 at 46 MHz to create Pr -> OK  |
| 11-53-03 | 100 kW | 46.0 MHz | repeat without SHAD with Pr/Pi set to 0.300 at 46 MHz to create Pr -> trigger  |
| 12-00-31 | 500 kW | 55.5 MHz | repeat without SHAD with Pr/Pi set to 0.300 at 55.5 MHz ok |
| 12-05-57 | 1000 kW | 55.5 MHz | repeat without SHAD with Pr/Pi set to 0.300 at 55.5 MHz ok |
| 12-15-17 | 1000 kW / 100ms | 55.5 MHz | no SHAD with Pr/Pi 0.300 measurement back in place |
| 12-30-50 | 1200 kW / 1s + 1s | 55.5 MHz | no SHAD with Pr/Pi 0.300 measurement back in place |
| 12-32-12 | 1500 kW / 1s + 1s | 55.5 MHz | no SHAD with Pr/Pi 0.300 measurement back in place |
| 12-33-24 | 1600 kW / 1s + 1s | 55.5 MHz | no SHAD with Pr/Pi 0.300 measurement back in place |
| 12-41-36 | 1600 kW / 1s + 1s | 55.5 MHz | no SHAD with Pr/Pi 0.300 measurement back in place |
| 12-47-21 | 1700 kW / 1.4s + 1s | 55.5 MHz | no SHAD with Pr/Pi 0.300 measurement back in place |
| 12-53-14 | 1750 kW / 2s + 1s | 55.5 MHz | no SHAD etc |
| 12-55-20 | 1800 kW / 2s + 1s | 55.5 MHz | no SHAD etc |
| 13-08-18 | 1800 kW / 2s + 1s | 55.5 MHz | no SHAD etc generator limitation  | 
| 13-12-37 | 1800 kW / 2s + 1s | 55.5 MHz | no SHAD etc increased dissipated power lim on gen  | 
| 13-18-32 | 1800 kW / 2s + 1s | 55.5 MHz | error in resuest : 1.8kW |
| 13-20-27 | 1800 kW / 2s + 1s | 55.5 MHz | repeat changing condig setup -> still limit |
| 13-22-24 | 1800 kW / 2s + 1s | 55.5 MHz | repeat changing config setup -> still limit -> will see tomorrow |
| :--: | :----------: | :--: | :-----: |
| 13-36-53 | 500 kW / 15s | 55.5 MHz | avec SHAD -> OK |
| 13-36-53 | 500 kW / 30s | 55.5 MHz | avec SHAD -> OK |
| 13-45-26 | 500 kW / 30s | 55.5 MHz | avec SHAD -> OK |
| 13-47-04 | 500 kW / 30s | 55.5 MHz | avec SHAD -> OK |
| 13-49-55 | 500 kW / 30s | 55.5 MHz | avec SHAD -> OK |
| 13-50-49 | 500 kW / 30s | 55.5 MHz | avec SHAD -> OK - line @ 42°C|
| 13-53-05 | 500 kW / 30s | 55.5 MHz | avec SHAD -> OK - line @ 47°C|
| :--: | :----------: | :--: | :-----: |
| 13-55-22 | 200 kW / 1s | 55.5 MHz | frequency scan at 50°C |
| 13-55-58 | 200 kW / 1s | 56.0 MHz | frequency scan at 50°C |
| 13-56-28 | 200 kW / 1s | 56.5 MHz | frequency scan at 50°C |
| 13-56-28 | 200 kW / 1s | 56.5 MHz | frequency scan at 50°C |
| 13-56-59 | 200 kW / 1s | 57.0 MHz | frequency scan at 50°C |
| 13-57-38 | 200 kW / 1s | 57.5 MHz | frequency scan at 50°C |
| 13-59-42 | 200 kW / 1s | 55.0 MHz | frequency scan at 50°C |
| 14-00-17 | 200 kW / 1s | 54.5 MHz | frequency scan at 50°C |
| 14-00-45 | 200 kW / 1s | 54.0 MHz | frequency scan at 50°C |
| 14-01-15 | 200 kW / 1s | 53.5 MHz | frequency scan at 50°C |
| 14-04-52 | 200 kW / 1s | 53.0 MHz | frequency scan at 50°C |
| 14-05-40 | 200 kW / 1s | 52.5 MHz | frequency scan at 50°C |
| 14-07-14 | 200 kW / 1s | 52.0 MHz | frequency scan at 50°C |
| 14-07-45 | 200 kW / 1s | 51.5 MHz | frequency scan at 50°C |
| 14-08-16 | 200 kW / 1s | 51.0 MHz | frequency scan at 50°C |
| 14-10-32 | 200 kW / 1s | 49.5 MHz | frequency scan at 50°C |
| 14-12-03 | 200 kW / 1s | 49.0 MHz | frequency scan at 50°C |
| 14-12-32 | 200 kW / 1s | 48.5 MHz | frequency scan at 50°C |
| 14-12-58 | 200 kW / 1s | 48.0 MHz | frequency scan at 50°C |
| 14-13-23 | 200 kW / 1s | 47.5 MHz | frequency scan at 50°C |
| 14-13-50 | 200 kW / 1s | 47.0 MHz | frequency scan at 50°C |
| 14-14-16 | 200 kW / 1s | 46.5 MHz | frequency scan at 50°C |
| 14-14-37 | 200 kW / 1s | 46.0 MHz | frequency scan at 50°C - No data, too much reflected power |
| 14-16-59 | 200 kW / 1s | 58.0 MHz | frequency scan at 50°C |
| 14-21-56 | 200 kW / 1s | 63.0 MHz | frequency scan at 50°C |
| 14-23-21 | 200 kW / 1s | 63.5 MHz | frequency scan at 50°C |
| 14-23-51 | 200 kW / 1s | 64.0 MHz | frequency scan at 50°C |
| 14-24-22 | 200 kW / 1s | 64.5 MHz | frequency scan at 50°C |
| 14-24-46 | 200 kW / 1s | 65.0 MHz | frequency scan at 50°C |
| 14-25-19 | 200 kW / 1s | 62.5 MHz | frequency scan at 50°C |
| 14-26-06 | 200 kW / 1s | 62.0 MHz | frequency scan at 50°C |
| 14-26-48 | 200 kW / 1s | 61.5 MHz | frequency scan at 50°C |
| 14-27-23 | 200 kW / 1s | 61.0 MHz | frequency scan at 50°C |
| 14-30-30 | 200 kW / 1s | 59.0 MHz | frequency scan at 50°C |
| 14-31-06 | 200 kW / 1s | 58.5 MHz | frequency scan at 50°C |
| 14-32-51 | 200 kW / 1s | 58.0 MHz | frequency scan at 50°C |
| :--: | :----------: | :--: | :-----: |
| 14- | 500 kW / 1s | 55.5 MHz | OK |
| 14- | 550 kW / 1s | 55.5 MHz | SHAD |
| 14- | 600 kW / 1s | 55.5 MHz | OK |
| 14- | 650 kW / 1s | 55.5 MHz | SHAD |
| 14- | 650 kW / 1s | 55.5 MHz | SHAD |
| 14- | 650 kW / 1s | 55.5 MHz | SHAD |
| 14- | 650 kW / 1s | 55.5 MHz | SHAD |
| :--: | :----------: | :--: | :-----: |
| 14-58-39 | 500 kW / 60s | 55.5 MHz | OK but 1 trip |
| 14-58-39 | 500 kW / 60s | 55.5 MHz | OK super clean |


