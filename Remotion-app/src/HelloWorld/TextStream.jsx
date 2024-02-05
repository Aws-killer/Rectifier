import React, {createElement} from 'react';
import {useVideoConfig, AbsoluteFill, TransitionSeries} from 'remotion';
import * as Fonts from '@remotion/google-fonts';
import transcriptData from './Assets/TextSequences.json';
import Constants from './Assets/Constants.json';
import {TransitionSeries} from '@remotion/transitions';
import {GsapAnimation} from './Components/GsapAnimation';
import gsap from 'gsap';
const defaultText = {
	fontFamily: 'Luckiest Guy',
	fontSize: 120,
	textAlign: 'center',
	textShadow:
		'-10px -10px 0 #000, 0   -10px 0 #000, 10px -10px 0 #000, 10px  0   0 #000, 10px  10px 0 #000, 0    10px 0 #000, -10px  10px 0 #000, -10px  0   0 #000',
	position: 'fixed',
	fontWeight: 'bolder',
	color: 'yellow',
	bottom: '30vh',
	height: 'fit-content',
	width: '100%',
};
const subtitle = Constants?.text
	? {
			...defaultText,
			...Constants.text,
	  }
	: defaultText;
Fonts.getAvailableFonts()
	.filter((font) => {
		return font.fontFamily === subtitle.fontFamily;
	})[0]
	.load()
	.then((font) => font.loadFont());

export const TextStream = () => {
	const {fps} = useVideoConfig();

	return (
		<AbsoluteFill
			style={{
				backgroundColor: 'transparent',
				justifyContent: 'center',
				alignItems: 'center',
				position: 'relative',
				// backgroundColor: 'red',
			}}
		>
			<TransitionSeries>
				{transcriptData.map((entry, index) => {
					const delta = entry.end - entry.start < 1 / 30 ? 0.2 : 0;
					return (
						<TransitionSeries.Sequence
							style={subtitle}
							key={index}
							from={(entry.start + delta) * fps}
							durationInFrames={fps * (entry.end - entry.start + delta)}
						>
							<Letter duration={(entry.end - entry.start + delta)} style={subtitle}>{entry.text}</Letter>
						</TransitionSeries.Sequence>
					);
				})}
			</TransitionSeries>
		</AbsoluteFill>
	);
};

export function Letter({children, style,duration}) {
	
	const Textimeline =()=>{
		let timeline=gsap.timeline()
		timeline.fromTo('#letter',{yPercent:100},{yPercent:0,duration:duration/2, ease:"power2.inOut"})		
		return timeline
		}
	
	return <GsapAnimation Timeline={Textimeline} className='h-fit' style={style}>
		
	
		<div id="letter">
			{children}
		</div>
		</GsapAnimation>;
}


