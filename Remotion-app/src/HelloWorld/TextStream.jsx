import React, {createElement} from 'react';
import {useVideoConfig, AbsoluteFill, TransitionSeries} from 'remotion';
import * as Fonts from '@remotion/google-fonts';
import transcriptData from './Assets/TextSequences.json';
import {FONT_FAMILY} from './constants';
import {TransitionSeries} from '@remotion/transitions';

const subtitle = {
	fontFamily: FONT_FAMILY,
	fontSize: 150,
	textAlign: 'center',
	textShadow:
		'-5px -5px 0 #00ff, 0   -5px 0 #00ff, 5px -5px 0 #00ff, 5px  0   0 #00ff, 5px  5px 0 #00ff, 0    5px 0 #00ff, -5px  5px 0 #00ff, -5px  0   0 #00ff',
	position: 'fixed',
	fontWeight: 'bolder',
	color: 'white',
	bottom: 200,
	height: 'fit-content',
	width: '100%',
};

Fonts.getAvailableFonts()
	.filter((font) => {
		return font.fontFamily === FONT_FAMILY;
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
					return (
						<TransitionSeries.Sequence
							style={subtitle}
							key={index}
							from={(entry.start + 0.2) * fps}
							durationInFrames={fps * (entry.end - entry.start + 0.2)}
						>
							<Letter style={subtitle}>{entry.text}</Letter>
						</TransitionSeries.Sequence>
					);
				})}
			</TransitionSeries>
		</AbsoluteFill>
	);
};

export function Letter({children, style}) {
	return <div style={style}>{children}</div>;
}
