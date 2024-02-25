import React, {useMemo} from 'react';
import {useVideoConfig, AbsoluteFill, TransitionSeries} from 'remotion';
import * as Fonts from '@remotion/google-fonts';
import transcriptData from './Assets/TextSequences.json';
import Constants from './Assets/Constants.json';
import {TransitionSeries} from '@remotion/transitions';
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

const TextStream = React.memo(() => {
	const {fps} = useVideoConfig();

	const memoizedTranscriptData = useMemo(() => {
		return transcriptData;
	}, []);

	return (
		<AbsoluteFill
			style={{
				backgroundColor: 'transparent',
				justifyContent: 'center',
				alignItems: 'center',
			}}
		>
			<TransitionSeries>
				{memoizedTranscriptData.map((entry, index) => {
					const delta = entry.end - entry.start < 1 / 30 ? 0.2 : 0;
					return (
						<TransitionSeries.Sequence
							style={subtitle}
							key={index}
							from={(entry.start + delta) * fps}
							durationInFrames={fps * (entry.end - entry.start + delta)}
						>
							<Letter style={subtitle}>{entry.text}</Letter>
						</TransitionSeries.Sequence>
					);
				})}
			</TransitionSeries>
		</AbsoluteFill>
	);
});

const Letter = React.memo(({children, style}) => {
	return <div style={style}>{children}</div>;
});

export default TextStream;
