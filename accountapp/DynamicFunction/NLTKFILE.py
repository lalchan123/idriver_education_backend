from transformers import T5Tokenizer, T5ForConditionalGeneration

def generate_summary(input_text):
    device = "cuda"
    model_name = "t5-base"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name).to(device)

    input_ids = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=512, truncation=True)
    summary_ids = model.generate(input_ids, max_length=150, num_beams=2, length_penalty=2.0, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

# Example usage
input_text = '''

Exxon Mobil

aims to become a leading producer of lithium for electric vehicle batteries through a drilling operation the oil giant is launching in Arkansas, the company announced Monday.

Exxon earlier this year purchased 120,000 acres of a geological site in southern Arkansas called the Smackover Formation that is rich in lithium.

The company will start producing battery-grade lithium at the site as soon as 2027, and aims to supply enough of the mineral to support the manufacture of 1 million electric vehicles annually by 2030.

Discussions with potential customers such as electric vehicle and battery manufacturers are ongoing, Exxon said in a statement.

The lithium operation comes as the major oil companies are under pressure to address climate change. While Shell and BP have focused on renewables such as wind and solar, Exxon is investing $17 billion through 2027 to reduce emissions with a focus on carbon capture, hydrogen and biofuels.

Dan Ammann, president of Exxon’s low carbon solutions business, told CNBC that ramping up domestic production of lithium is crucial to the energy transition. Exxon views lithium as a decadeslong investment with high growth potential as the U.S. shifts to electric vehicles, Ammann said.

“We want to get in early,” Ammann told CNBC’s “Squawk Box.” “We want to lead the way on domestic production of lithium, do it with a very favorable environmental footprint and set that as the standard.”

The U.S. is heavily reliant on imports from Argentina and Chile for its lithium needs despite having some of the largest deposits of the mineral in the world, according to the U.S. Geological Survey. The U.S currently has just one commercial-scale lithium production operation, in Nevada.

Demand for lithium batteries is expected to surge sixfold in the U.S. by 2030 as the nation shifts to electric vehicles, according to a February report from Li-Bridge, a battery industry group backed by the Department of Energy.

Electric vehicles sales grew 50% in the third quarter of 2023 compared with the same period last year, according to an October report from Cox Automotive. Currently, just 1% of the U.S. vehicle fleet is electric.

“We need to get obviously to a much higher percentage in the long run,” Ammann said. “It’s going to be very high growth, sustained for a very long time. That may have some ups and downs and some fits and starts as we go, but again, we see very much long-term opportunity for playing the long-term game here.”

Exxon is deploying drilling techniques used in oil and gas extraction to access saltwater reservoirs rich in lithium that are 10,000 feet below ground. The lithium is separated from the saltwater and turned into battery-grade material onsite, according to the company.

The lithium battery was invented by a research scientist at Exxon in the 1970s but the oil giant ultimately didn’t pursue the technology.


'''
summary = generate_summary(input_text)
print("Original Text:", input_text)
print("Summary1:", summary)
summary = generate_summary(summary)
print("Summary2:", summary)
summary = generate_summary(summary)
print("Summary3:", summary)