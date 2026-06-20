# repro/chemistry/07-low-grade-waste-heat-electricity/
# VP Chemistry & EM §7 - Low-grade waste heat to electricity
# Each module: python3 <module>.py  ->  prints 'RESULT sha256 = ...'  (run twice -> identical).
# DOI: 10.5281/zenodo.20680540
#
# module                                  | expected sha256 prefix | verifies
# vp_magnet_lorentz.py                      | 7c8246ab               | CA.9a: static B does no work; cyclotron ensemble drift~0, KE constant; an E-field drives current
# vp_heatpump_exergy.py                     | 64e26ee6               | CA.9b: exergy ceiling 1-T0/T; heat-pump+engine loop net -65% (COP*eta_Carnot=1)
# vp_blackcu_absorber_not_generator.py      | 0067cbe1               | CA.9c: black copper is an absorber (alpha~0.96), no heat->electricity mechanism; melts at 1085C
# vp_thermomagnetic_oscillator.py           | d6d8a9ab               | CA.10: self-sustained relaxation oscillation; positive cycle-averaged harvested power
# vp_thermomagnetic_design.py               | 0a3af6ec               | CA.10: bare-device eta~0.4% at dT=25K (sensible+latent heat is the loss)
# vp_thermomagnetic_regenerative.py         | aa45e145               | CA.11: regenerative eta=Carnot/(1+(1-eps)R); 2.7% at eps=0.9, 4.0% at eps=0.95
# vp_regenerator_microchannel.py            | aa296c82               | CA.11: eps=K/(K+f), pumping 48*mu*f*L^2/(dc*tp*w); practical eta 2.6-4.4% at 1.5-4 Hz
# vp_datacenter_economics.py                | 13d054c5               | CA.12: 1 MW DC -> ~23 kW, ~205 MWh/yr, payback ~4-6 yr
# vp_waste_heat_scale.py                    | b59d22a5               | CA.12: per-AC ~9% offset; India fleet ~30 TWh/yr; efficiency saves 3-4x more
